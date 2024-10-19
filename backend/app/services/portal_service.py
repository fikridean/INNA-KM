from typing import List, Set
from pymongo import UpdateOne

from models.portal_model import (
    PortalCreateModel,
    PortalCreateResponseModelObject,
    PortalDeleteModel,
    PortalDeleteResponseModelObject,
    PortalDetailModel,
    PortalDetailResponseModelObject,
    PortalGetModel,
    PortalGetResponseModelObject,
    PortalRetrieveDataModel,
    PortalRetrieveDataResponseModelObject,
)
from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import (
    checkUnsupportedWeb,
    run_function_from_module,
    portal_webs,
)
from database.mongo import client, portal_collection, taxon_collection, raw_collection
from utils.enum.status_code_enum import StatusCode
from utils.enum.message_enum import ResponseMessage, StatusMessage, InfoMessage


@log_function("Create portal")
async def create_portal(
    params: List[PortalCreateModel],
) -> List[PortalCreateResponseModelObject]:
    # Validate input parameters
    if not params:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # Check for unsupported web sources
    unsupported_webs: List[str] = checkUnsupportedWeb(
        [web for portal in params for web in portal.web]
    )
    if unsupported_webs:
        raise Exception(
            {
                "data": [],
                "message": f"Web sources not supported: {', '.join(unsupported_webs)}.",
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # Check if the payload is empty
    if not params:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    result: List[PortalCreateResponseModelObject] = []

    portal_to_store: List[PortalCreateModel] = params.copy()

    # Check if portal_id not in database, but taxon_id is in database, then dont store
    portal_cannot_be_stored: List[PortalCreateModel] = []

    for portal in portal_to_store:
        if not await portal_collection.find_one(
            {"portal_id": portal.portal_id}, {"_id": 0}
        ):
            if await portal_collection.find_one(
                {"taxon_id": portal.taxon_id}, {"_id": 0}
            ):
                portal_to_store.remove(portal)
                portal_cannot_be_stored.append(portal)

    # Prepare operations and check for missing taxons
    operations: List[UpdateOne] = []

    for portal in portal_to_store:
        # Append the update operation
        operations.append(
            UpdateOne(
                {"portal_id": portal.portal_id},
                {
                    "$set": {
                        "portal_id": portal.portal_id,
                        "taxon_id": portal.taxon_id,
                        "web": portal.web,
                    }
                },
                upsert=True,
            )
        )

    # Execute operations in a transaction
    async with await client.start_session() as session:
        async with session.start_transaction():
            await portal_collection.bulk_write(operations, session=session)

    # Prepare the result response
    result += [
        PortalCreateResponseModelObject(
            portal_id=portal.portal_id,
            taxon_id=portal.taxon_id,
            web=portal.web,
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_CREATED.value,
        )
        for portal in portal_to_store
    ] + [
        PortalCreateResponseModelObject(
            portal_id=portal.portal_id,
            taxon_id=portal.taxon_id,
            web=portal.web,
            status=StatusMessage.DATA_FAILED.value,
            info=f"{InfoMessage.DATA_NOT_CREATED.value}: {InfoMessage.PORTAL_WITH_TAXON_ID_EXIST.value}",
        )
        for portal in portal_cannot_be_stored
    ]

    return result


@log_function("Get portals")
async def get_portals(params: PortalGetModel) -> List[PortalGetResponseModelObject]:
    portal_id_for_query: List[int] = params.portal_id or []

    # Prepare query to fetch portals from the database
    query: dict = (
        {"portal_id": {"$in": portal_id_for_query}} if portal_id_for_query else {}
    )

    # Fetch portals from the database
    portals: List[dict] = await portal_collection.find(query, {"_id": 0}).to_list(
        length=None
    )

    # Gather found portal_ids
    found_portal_ids: Set[str] = {portal["portal_id"] for portal in portals}

    # Gather missing portal_ids
    if portal_id_for_query:
        missing_portals: Set[int] = set(portal_id_for_query) - found_portal_ids

    # Prepare the result response
    result: List[PortalGetResponseModelObject] = [
        PortalGetResponseModelObject(
            portal_id=portal["portal_id"],
            taxon_id=portal.get("taxon_id"),
            web=portal.get("web"),
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_RETRIEVED.value,
        )
        for portal in portals
    ] + [
        PortalGetResponseModelObject(
            portal_id=portal_id,
            taxon_id=None,
            web=None,
            status=StatusMessage.DATA_FAILED.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",
        )
        for portal_id in missing_portals
    ]

    return result


@log_function("Get portal detail")
async def get_portal_detail(
    params: PortalDetailModel,
) -> PortalDetailResponseModelObject:

    # prepare query
    portal_id_for_query: List[int] = params.portal_id or []

    # Fetch portal from the database
    portal: dict = await portal_collection.find_one(
        {"portal_id": portal_id_for_query}, {"_id": 0}
    )

    # Prepare the result response
    # If portal is not found, return a response with status and info
    if not portal:
        return PortalDetailResponseModelObject(
            portal_id=portal_id_for_query,
            taxon_id=None,
            web=None,
            status=StatusMessage.DATA_FAILED.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",
        )

    # If portal is found, return a response with the portal details
    return PortalDetailResponseModelObject(
        portal_id=portal["portal_id"],
        taxon_id=portal.get("taxon_id"),
        web=portal.get("web"),
        status=StatusMessage.DATA_SUCCESS.value,
        info=InfoMessage.DATA_RETRIEVED.value,
    )


@log_function("Delete portal")
async def delete_portal(
    params: PortalDeleteModel,
) -> List[PortalDeleteResponseModelObject]:

    # prepare query
    portal_id_for_query: List[int] = params.portal_id or []

    # If portal_id is not provided, return an error
    if not portal_id_for_query:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    async with await client.start_session() as session:
        async with session.start_transaction():

            # Fetch portals from the database
            portals: dict = await portal_collection.find(
                {"portal_id": {"$in": portal_id_for_query}}, {"_id": 0}, session=session
            ).to_list(length=None)

            # Gather found portal_ids
            found_portal_ids: Set[int] = {portal["portal_id"] for portal in portals}

            # Check if any of the portal_ids are used in the raw_collection
            used_portal_ids: List[int] = await raw_collection.distinct(
                "portal_id",
                {"portal_id": {"$in": list(found_portal_ids)}},
                session=session,
            )

            # Gather not used portal_ids
            not_used_portal_ids: List[int] = list(
                found_portal_ids - set(used_portal_ids)
            )

            # Delete the portals from the database
            await portal_collection.delete_many(
                {"portal_id": {"$in": list(found_portal_ids - set(used_portal_ids))}},
                session=session,
            )

    # Gather not found portal_ids
    portals_not_found: List[str] = [
        portal_id
        for portal_id in portal_id_for_query
        if portal_id not in found_portal_ids
    ]

    # Prepare the result response
    # If portal is not used in raw_collection, return a response with status and info
    result: List[PortalDeleteResponseModelObject] = (
        [
            PortalDeleteResponseModelObject(
                portal_id=portal["portal_id"],
                taxon_id=portal.get("taxon_id"),
                web=portal.get("web"),
                status=StatusMessage.DATA_SUCCESS.value,
                info=InfoMessage.DATA_DELETED.value,
            )
            for portal in portals
            if portal["portal_id"] in not_used_portal_ids
        ]
        + [  # If portal is used in raw_collection, return a response with status and info
            PortalDeleteResponseModelObject(
                portal_id=portal["portal_id"],
                taxon_id=portal.get("taxon_id"),
                web=portal.get("web"),
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.PORTAL_USED.value}.",
            )
            for portal in portals
            if portal["portal_id"] in used_portal_ids
        ]
        + [  # If portal is not found, return a response with status and info
            PortalDeleteResponseModelObject(
                portal_id=portal_id,
                taxon_id=None,
                web=None,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",
            )
            for portal_id in portals_not_found
        ]
    )

    return result


@log_function("Retrieve data")
async def retrieve_data(
    params: PortalRetrieveDataModel,
) -> PortalRetrieveDataResponseModelObject:

    # Validate input parameters
    if not params:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    ncbi_taxon_id_for_query: List[int] = params.ncbi_taxon_id or []
    web_for_query: List[str] = params.web or []

    # Check if ncbi_taxon_id and web are provided
    if not ncbi_taxon_id_for_query or not web_for_query:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # Check for unsupported web sources
    if web_for_query not in portal_webs:
        raise Exception(
            {
                "data": [],
                "message": f"Web source not supported: {web_for_query}.",
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # prepare query
    ncbi_taxon_id_for_query: List[int] = ncbi_taxon_id_for_query or []

    async with await client.start_session() as session:
        async with session.start_transaction():

            # fetch taxon from database
            taxon: dict = await taxon_collection.find_one(
                {"ncbi_taxon_id": ncbi_taxon_id_for_query}, {"_id": 0}, session=session
            )

            # Return not found message if taxon not found
            if not taxon:
                return PortalRetrieveDataResponseModelObject(
                    portal_id=None,
                    taxon_id=None,
                    web=params.web,
                    data={},
                    status=StatusMessage.DATA_FAILED.value,
                    info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}",
                )

            # fetch portal from database
            portal: dict = await portal_collection.find_one(
                {"taxon_id": taxon.get("taxon_id"), "web": params.web},
                {"_id": 0},
                session=session,
            )

    # Return not found message if portal not found
    if not portal:
        return PortalRetrieveDataResponseModelObject(
            portal_id=None,
            taxon_id=taxon.get("taxon_id"),
            web=params.web,
            data={},
            status=StatusMessage.DATA_FAILED.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",
        )

    # Return data if found
    return PortalRetrieveDataResponseModelObject(
        portal_id=portal.get("portal_id"),
        taxon_id=taxon.get("taxon_id"),
        web=params.web,
        data=await run_function_from_module(params.web, "retrieve", taxon),
        status=(
            StatusMessage.DATA_SUCCESS.value
            if taxon
            else StatusMessage.DATA_FAILED.value
        ),
        info=(
            InfoMessage.DATA_RETRIEVED.value
            if taxon
            else InfoMessage.DATA_NOT_RETRIEVED.value
        ),
    )
