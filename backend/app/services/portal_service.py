from typing import List, Set
from pymongo import UpdateOne

from models.portal_model import (
    PortalCreateModel, PortalCreateResponseModelObject,
    PortalDeleteModel, PortalDeleteResponseModelObject,
    PortalDetailModel, PortalDetailResponseModelObject,
    PortalGetModel, PortalGetResponseModelObject,
    PortalRetrieveDataModel, PortalRetrieveDataResponseModelObject,
)
from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import run_function_from_module, portal_webs
from database.mongo import client, portal_collection, taxon_collection, raw_collection
from utils.enum.status_code_enum import StatusCode
from utils.enum.message_enum import ResponseMessage, StatusMessage, InfoMessage

@log_function("Create portal")
async def create_portal(params: List[PortalCreateModel]) -> List[PortalCreateResponseModelObject]:
    # Validate input parameters
    if not params:
        raise Exception({
            "data": [],
            "message": ResponseMessage.INVALID_PAYLOAD.value,
            "status_code": StatusCode.BAD_REQUEST.value
        })

    # Check for unsupported web sources
    unsupported_webs: List[str] = [
        web for portal in params for web in portal.web if web not in portal_webs
    ]
    if unsupported_webs:
        raise Exception({
            "data": [],
            "message": f"Web sources not supported: {', '.join(unsupported_webs)}.",
            "status_code": StatusCode.BAD_REQUEST.value
        })

    # Gather taxon_ids to check their existence
    taxon_ids: List[str] = [portal.taxon_id for portal in params]

    # Check for existing taxon_ids in the taxon_collection
    existing_taxons: List[dict] = await taxon_collection.find(
        {"taxon_id": {"$in": taxon_ids}},
        {'_id': 0}
    ).to_list(length=None)

    existing_taxon_ids: set = {taxon['taxon_id'] for taxon in existing_taxons}

    # Prepare operations and check for missing taxons
    operations: List[UpdateOne] = []
    for portal in params:
        if portal.taxon_id not in existing_taxon_ids:
            raise Exception({
                "data": [],
                "message": f"Taxon ID {portal.taxon_id} does not exist in the taxon collection.",
                "status_code": StatusCode.BAD_REQUEST.value
            })
        # Append the update operation
        operations.append(UpdateOne(
            {"portal_id": portal.portal_id},
            {"$set": {
                "portal_id": portal.portal_id,
                "taxon_id": portal.taxon_id,
                "web": portal.web
            }},
            upsert=True
        ))

    # Execute operations in a transaction
    async with await client.start_session() as session:
        async with session.start_transaction():
            await portal_collection.bulk_write(operations, session=session)

    # Prepare the result response
    result: List[PortalCreateResponseModelObject] = [
        PortalCreateResponseModelObject(
            portal_id=portal.portal_id,
            taxon_id=portal.taxon_id,
            web=portal.web,
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_CREATED.value
        ) for portal in params
    ]

    return result

@log_function("Get portals")
async def get_portals(params: PortalGetModel) -> List[PortalGetResponseModelObject]:
    query: dict = {"portal_id": {'$in': params.portal_id}} if params.portal_id else {}
    portals: List[dict] = await portal_collection.find(query, {'_id': 0}).to_list(length=None)

    found_portal_ids: Set[str] = {portal['portal_id'] for portal in portals}

    result: List[PortalGetResponseModelObject] = [
        PortalGetResponseModelObject(
            portal_id=portal['portal_id'],
            taxon_id=portal.get('taxon_id'),
            web=portal.get('web'),
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_RETRIEVED.value
        ) for portal in portals
    ]

    if params.portal_id:
        missing_portals: set = set(params.portal_id) - found_portal_ids
        result.extend([
            PortalGetResponseModelObject(
                portal_id=portal_id,
                taxon_id=None,
                web=None,
                status=StatusMessage.DATA_NOT_FOUND.value,
                info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}"
            ) for portal_id in missing_portals
        ])

    return result

@log_function("Get portal detail")
async def get_portal_detail(params: PortalDetailModel) -> PortalDetailResponseModelObject:
    portal: dict = await portal_collection.find_one({"portal_id": params.portal_id}, {'_id': 0})

    if not portal:
        return PortalDetailResponseModelObject(
            portal_id=params.portal_id,
            taxon_id=None,
            web=None,
            status=StatusMessage.DATA_NOT_FOUND.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}"
        )

    return PortalDetailResponseModelObject(
        portal_id=portal['portal_id'],
        taxon_id=portal.get('taxon_id'),
        web=portal.get('web'),
        status=StatusMessage.DATA_SUCCESS.value,
        info=InfoMessage.DATA_RETRIEVED.value
    )

@log_function("Delete portal")
async def delete_portal(params: PortalDeleteModel):
    if not params.portal_id:
        raise Exception({
            "data": [],
            "message": ResponseMessage.INVALID_PAYLOAD.value,
            "status_code": StatusCode.BAD_REQUEST.value
        })
    
    async with await client.start_session() as session:
        async with session.start_transaction():
            portals: dict = await portal_collection.find({
                "portal_id": {"$in": params.portal_id}
            }, {'_id': 0}, session=session).to_list(length=None)

            found_portal_ids: set = {portal['portal_id'] for portal in portals}

            used_portal_ids = await raw_collection.distinct(
                'portal_id',
                {'portal_id': {'$in': list(found_portal_ids)}},
                session=session
            )

            if used_portal_ids:
                raise Exception({
                    "data": [],
                    "message": f"{ResponseMessage.PORTAL_USED.value}: {used_portal_ids}",
                    "status_code": StatusCode.BAD_REQUEST.value
                })

            await portal_collection.delete_many({"portal_id": {"$in": params.portal_id}}, session=session)

    portals_not_found: List[str] = [portal_id for portal_id in params.portal_id if portal_id not in found_portal_ids]

    result: List[PortalDeleteResponseModelObject] = [
        PortalDeleteResponseModelObject(
            portal_id=portal['portal_id'],
            taxon_id=portal['taxon_id'],
            web=portal['web'],
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_DELETED.value
        ) for portal in portals
    ] + [
        PortalDeleteResponseModelObject(
            portal_id=portal_id,
            taxon_id=None,
            web=None,
            status=StatusMessage.DATA_NOT_FOUND.value,
            info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}"
        ) for portal_id in portals_not_found
    ]
    return result

@log_function("Retrieve data")
async def retrieve_data(params: PortalRetrieveDataModel) -> PortalRetrieveDataResponseModelObject:
    if not params:
        raise Exception({
            "data": [],
            "message": ResponseMessage.INVALID_PAYLOAD.value,
            "status_code": StatusCode.BAD_REQUEST.value
        })
    
    if not params.ncbi_taxon_id or not params.web:
        raise Exception({
            "data": [],
            "message": ResponseMessage.INVALID_PAYLOAD.value,
            "status_code": StatusCode.BAD_REQUEST.value
        })
    
    if params.web not in portal_webs:
        raise Exception({
            "data": [],
            "message": f"Web source not supported: {params.web}.",
            "status_code": StatusCode.BAD_REQUEST.value
        })
    
    async with await client.start_session() as session:
        async with session.start_transaction():
            taxon: dict = await taxon_collection.find_one({"ncbi_taxon_id": params.ncbi_taxon_id}, {'_id': 0}, session=session)

            if not taxon:
                return PortalRetrieveDataResponseModelObject(
                    portal_id=None,
                    taxon_id=None,
                    web=params.web,
                    data={},
                    status=StatusMessage.DATA_NOT_FOUND.value,
                    info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}"
                )

            portal: dict = await portal_collection.find_one({"taxon_id": taxon.get('taxon_id'), "web": params.web}, {'_id': 0}, session=session)

    if not portal:
        return PortalRetrieveDataResponseModelObject(
            portal_id=None,
            taxon_id=taxon.get('taxon_id'),
            web=params.web,
            data={},
            status=StatusMessage.DATA_NOT_FOUND.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}"
        )

    return PortalRetrieveDataResponseModelObject(
        portal_id=portal.get('portal_id'),
        taxon_id=taxon.get('taxon_id'),
        web=params.web,
        data=await run_function_from_module(params.web, "retrieve", taxon),
        status=StatusMessage.DATA_SUCCESS.value if taxon else StatusMessage.DATA_NOT_FOUND.value,
        info=InfoMessage.DATA_RETRIEVED.value if taxon else InfoMessage.DATA_NOT_RETRIEVED.value
    )
    
