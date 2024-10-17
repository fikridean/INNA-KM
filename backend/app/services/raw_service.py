from typing import Any, List, Set, Tuple, Dict

from pymongo import UpdateOne
from utils.enum.status_code_enum import StatusCode
from utils.enum.message_enum import (
    SpeciesMessage,
    StatusMessage,
    InfoMessage,
)
from models.portal_model import (
    PortalRetrieveDataModel,
    PortalRetrieveDataResponseModelObject,
)
from models.raw_model import (
    RawDeleteModel,
    RawDeleteResponseModelObject,
    RawGetModel,
    RawGetResponseModelObject,
    RawStoreModel,
    RawStoreResponseModelObject,
)
from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import (
    checkUnsupportedWeb,
    run_function_from_module,
    portal_webs,
)
from database.mongo import client, raw_collection, taxon_collection, portal_collection
from .portal_service import retrieve_data


# Helper to filter webs for processing
def filter_webs_for_processing(
    portal_webs: List[str], web_for_query: List[str]
) -> List[str]:
    """Returns a list of webs that are present in both portal webs and the query."""
    return list(set(portal_webs).intersection(set(web_for_query)))


# Store raw from portals to raw collection
@log_function("Store raw from portals")
async def store_raw_from_portals(
    params: RawStoreModel,
) -> List[RawStoreResponseModelObject]:
    # prepare query parameters
    ncbi_taxon_id_for_query: List[str] = params.ncbi_taxon_id
    web_for_query: List[str] = params.web or portal_webs

    # Check for unsupported web sources
    unsupported_webs: List[str] = checkUnsupportedWeb(web_for_query)
    if unsupported_webs:
        raise Exception(
            {
                "data": [],
                "message": f"Web sources not supported: {', '.join(unsupported_webs)}.",
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # Retrieve taxa
    taxa: List[dict] = await taxon_collection.find(
        {  # List of taxon dictionaries
            "ncbi_taxon_id": {"$in": ncbi_taxon_id_for_query}
        },
        {"_id": 0},
    ).to_list(length=None)

    # Determine taxa not found
    taxa_not_found: Set[str] = set(ncbi_taxon_id_for_query) - {
        taxon["ncbi_taxon_id"] for taxon in taxa
    }

    # Prepare data structures
    data_to_store: List[dict] = []
    found_taxon_web: dict = {
        taxon["ncbi_taxon_id"]: {
            "taxon_id": taxon["taxon_id"],
            "species": taxon["species"],
            "found_webs": {"exist": [], "not_exist": []},
            "missing_webs": set(web_for_query),
            "status": StatusMessage.DATA_FAILED.value,
            "info": InfoMessage.DATA_NOT_RETRIEVED_AND_STORED.value,
        }
        for taxon in taxa
    }

    # Retrieve taxon portals
    taxon_ids: List[str] = [taxon["taxon_id"] for taxon in taxa]
    portals: List[dict] = await portal_collection.find(
        {"taxon_id": {"$in": taxon_ids}},
        {"_id": 0, "taxon_id": 1, "portal_id": 1, "web": 1},
    ).to_list(length=None)

    # Create a map of taxon_id to portal
    portal_map: dict = {portal["taxon_id"]: portal for portal in portals}

    # Process each taxon
    for taxon in taxa:
        # Check if portal exists for taxon
        portal: dict = portal_map.get(taxon["taxon_id"])
        if portal:
            # Store portal_id in taxon
            taxon["portal_id"] = portal["portal_id"]

            # Process each web
            web_need_to_process: List[str] = filter_webs_for_processing(
                portal["web"], web_for_query
            )

            for web in web_need_to_process:

                # Retrieve data from portal
                params: PortalRetrieveDataModel = PortalRetrieveDataModel(
                    ncbi_taxon_id=taxon["ncbi_taxon_id"], web=web
                )
                retrieved_data: PortalRetrieveDataResponseModelObject = (
                    await retrieve_data(params)
                )

                # Store data if retrieved
                if retrieved_data:
                    retrieved_data = retrieved_data.data

                    # Store found data
                    found_taxon_web[taxon["ncbi_taxon_id"]]["found_webs"][
                        "exist"
                    ].append(
                        {
                            "web": web,
                            "status": StatusMessage.DATA_FOUND.value,
                            "info": InfoMessage.DATA_RETRIEVED_AND_STORED.value,
                        }
                    )
                    data_to_store.append(
                        {
                            "portal_id": taxon.get("portal_id"),
                            "web": web,
                            "data": await run_function_from_module(
                                web, "data_processing", retrieved_data
                            ),
                        }
                    )
                else:
                    # Store not found data
                    found_taxon_web[taxon["ncbi_taxon_id"]]["found_webs"][
                        "not_exist"
                    ].append(
                        {
                            "web": web,
                            "status": StatusMessage.DATA_NOT_FOUND.value,
                            "info": InfoMessage.DATA_NOT_RETRIEVED_AND_STORED.value,
                        }
                    )

                # Remove web from missing webs
                found_taxon_web[taxon["ncbi_taxon_id"]]["missing_webs"].discard(web)

    async with await client.start_session() as session:
        async with session.start_transaction():
            # Bulk write data to raw collection
            bulk_operations = []
            for data in data_to_store:
                bulk_operations.append(
                    UpdateOne(
                        {
                            "portal_id": data["portal_id"],
                            "web": data["web"],
                        },
                        {"$set": data},
                        upsert=True,
                    )
                )

            # Execute bulk operations in one go
            if bulk_operations:  # Ensure there are operations to execute
                await raw_collection.bulk_write(bulk_operations, session=session)

    # Prepare final result
    result: List[RawStoreResponseModelObject] = []
    for ncbi_taxon_id, details in found_taxon_web.items():
        # Determine status and info
        if not details["found_webs"]["exist"]:
            # No data found
            details["status"] = StatusMessage.DATA_FAILED.value
            details["info"] = (
                InfoMessage.DATA_NOT_RETRIEVED_AND_STORED_FROM_ALL_WEB.value
            )
        elif len(details["found_webs"]["exist"]) == len(web_for_query):
            # All data found
            details["status"] = StatusMessage.DATA_SUCCESS.value
            details["info"] = InfoMessage.DATA_RETRIEVED_AND_STORED_FROM_ALL_WEB.value

        result.append(
            RawStoreResponseModelObject(
                taxon_id=details["taxon_id"],
                ncbi_taxon_id=ncbi_taxon_id,
                species=details["species"],
                found_webs=details["found_webs"],
                missing_webs=list(details["missing_webs"]),
                status=details["status"],
                info=details["info"],
            )
        )

    result.extend(
        [
            RawStoreResponseModelObject(
                taxon_id=None,
                ncbi_taxon_id=ncbi_taxon_id,
                species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                found_webs={"exist": [], "not_exist": []},
                missing_webs=web_for_query.copy(),
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_RETRIEVED_AND_STORED.value}: {InfoMessage.TAXON_NOT_EXIST.value}",
            )
            for ncbi_taxon_id in taxa_not_found
        ]
    )

    return result


# Get raw from raw collection
@log_function("Get raw from raw collection")
async def get_raw(params: RawGetModel) -> List[RawGetResponseModelObject]:

    # Extract necessary parameters
    ncbi_taxon_id__for_query: List[str] = params.ncbi_taxon_id
    web_for_query: List[str] = params.web or portal_webs

    # Build query for taxa
    query_ncbi_taxon_id: dict = (
        {"ncbi_taxon_id": {"$in": ncbi_taxon_id__for_query}}
        if ncbi_taxon_id__for_query
        else {}
    )

    # Check for unsupported web sources
    unsupported_webs: List[str] = checkUnsupportedWeb(web_for_query)
    if unsupported_webs:
        raise Exception(
            {
                "data": [],
                "message": f"Web sources not supported: {', '.join(unsupported_webs)}.",
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # Retrieve taxa
    taxa: List[dict] = await taxon_collection.find(
        query_ncbi_taxon_id, {"_id": 0}
    ).to_list(length=None)

    # Extract ncbi_taxon_ids and taxon_ids from taxa
    ncbi_taxon_ids = [taxon["ncbi_taxon_id"] for taxon in taxa]
    taxon_ids = [taxon["taxon_id"] for taxon in taxa]

    # Find taxa not found in the database
    not_found_taxa = [
        ncbi_id for ncbi_id in ncbi_taxon_id__for_query if ncbi_id not in ncbi_taxon_ids
    ]

    # Retrieve portals
    portals = await portal_collection.find(
        {"taxon_id": {"$in": taxon_ids}}, {"_id": 0}
    ).to_list(length=None)

    # Create maps for easy lookup
    portal_map = {portal["taxon_id"]: portal["portal_id"] for portal in portals}
    taxa_with_no_portal = [
        taxon for taxon in taxa if taxon["taxon_id"] not in portal_map
    ]

    # Update taxa with portal_id
    for taxon in taxa:
        taxon["portal_id"] = portal_map.get(taxon["taxon_id"])

    # Prepare to retrieve raw data
    portal_ids = [taxon["portal_id"] for taxon in taxa if taxon.get("portal_id")]
    raws = await raw_collection.find(
        {"portal_id": {"$in": portal_ids}, "web": {"$in": web_for_query}}, {"_id": 0}
    ).to_list(length=None)

    # Create raw data map
    raw_map = {}
    for raw in raws:
        raw_key = (raw["portal_id"], raw["web"])
        raw_map.setdefault(raw_key, []).append(raw)

    # Prepare results
    result: List[RawGetResponseModelObject] = []

    # Process each taxon
    for taxon in taxa:
        portal_id = taxon.get("portal_id")
        if not portal_id:
            continue

        found_webs = set()
        web_need_to_process = filter_webs_for_processing(portal_webs, web_for_query)

        for web in web_need_to_process:
            raw_key = (portal_id, web)
            if raw_key in raw_map:
                for raw in raw_map[raw_key]:
                    result.append(
                        RawGetResponseModelObject(
                            taxon_id=taxon["taxon_id"],
                            ncbi_taxon_id=taxon["ncbi_taxon_id"],
                            species=taxon["species"],
                            web=web,
                            data=raw["data"],
                            status=StatusMessage.DATA_SUCCESS.value,
                            info=InfoMessage.DATA_RETRIEVED.value,
                        )
                    )
                found_webs.add(web)

        # Handle missing webs
        missing_webs = set(web_for_query) - found_webs
        for web in missing_webs:
            result.append(
                RawGetResponseModelObject(
                    taxon_id=taxon["taxon_id"],
                    ncbi_taxon_id=taxon["ncbi_taxon_id"],
                    species=taxon["species"],
                    web=web,
                    data=None,
                    status=StatusMessage.DATA_FAILED.value,
                    info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.RAW_NOT_EXIST.value}",
                )
            )

    # Append not found taxa
    result.extend(
        [
            RawGetResponseModelObject(
                ncbi_taxon_id=ncbi_id,
                species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                web=None,
                data=None,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}",
            )
            for ncbi_id in not_found_taxa
        ]
    )

    # Append taxa with no portal
    result.extend(
        [
            RawGetResponseModelObject(
                taxon_id=taxon["taxon_id"],
                ncbi_taxon_id=taxon["ncbi_taxon_id"],
                species=taxon["species"],
                web=None,
                data=None,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",
            )
            for taxon in taxa_with_no_portal
        ]
    )

    return result


# Delete raw from raw collection
@log_function("Delete raw from raw collection")
async def delete_raw_from_db(
    params: RawDeleteModel,
) -> List[RawDeleteResponseModelObject]:
    # Extract necessary parameters
    ncbi_taxon_id__for_query: List[str] = params.ncbi_taxon_id
    web_for_query: List[str] = params.web or portal_webs

    # Build query for taxa
    query_ncbi_taxon_id: dict = (
        {"ncbi_taxon_id": {"$in": ncbi_taxon_id__for_query}}
        if ncbi_taxon_id__for_query
        else {}
    )

    # Check for unsupported web sources
    unsupported_webs: List[str] = checkUnsupportedWeb(web_for_query)
    if unsupported_webs:
        raise Exception(
            {
                "data": [],
                "message": f"Web sources not supported: {', '.join(unsupported_webs)}.",
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # Retrieve taxa
    taxa: List[dict] = await taxon_collection.find(
        query_ncbi_taxon_id, {"_id": 0}
    ).to_list(length=None)

    # Extract ncbi_taxon_ids and taxon_ids from taxa
    ncbi_taxon_ids = [taxon["ncbi_taxon_id"] for taxon in taxa]
    taxon_ids = [taxon["taxon_id"] for taxon in taxa]

    # Find taxa not found in the database
    not_found_taxa = [
        ncbi_id for ncbi_id in ncbi_taxon_id__for_query if ncbi_id not in ncbi_taxon_ids
    ]

    # Retrieve portals
    portals = await portal_collection.find(
        {"taxon_id": {"$in": taxon_ids}}, {"_id": 0}
    ).to_list(length=None)

    # Create maps for easy lookup
    portal_map = {portal["taxon_id"]: portal["portal_id"] for portal in portals}
    taxa_with_no_portal = [
        taxon for taxon in taxa if taxon["taxon_id"] not in portal_map
    ]

    # Update taxa with portal_id
    for taxon in taxa:
        taxon["portal_id"] = portal_map.get(taxon["taxon_id"])

    # Prepare to retrieve raw data
    portal_ids = [taxon["portal_id"] for taxon in taxa if taxon.get("portal_id")]
    raws = await raw_collection.find(
        {"portal_id": {"$in": portal_ids}, "web": {"$in": web_for_query}}, {"_id": 0}
    ).to_list(length=None)

    # Create raw data map
    raw_map = {}
    for raw in raws:
        raw_key = (raw["portal_id"], raw["web"])
        raw_map.setdefault(raw_key, []).append(raw)

    # Prepare results
    result: List[RawDeleteResponseModelObject] = []

    # Process each taxon
    for taxon in taxa:
        portal_id = taxon.get("portal_id")
        if not portal_id:
            continue

        found_webs = set()
        web_need_to_process = filter_webs_for_processing(portal_webs, web_for_query)

        for web in web_need_to_process:
            raw_key = (portal_id, web)
            if raw_key in raw_map:
                for raw in raw_map[raw_key]:
                    async with await client.start_session() as session:
                        async with session.start_transaction():
                            await raw_collection.delete_one(
                                {"portal_id": raw["portal_id"], "web": raw["web"]}
                            )

                    result.append(
                        RawDeleteResponseModelObject(
                            taxon_id=taxon["taxon_id"],
                            ncbi_taxon_id=taxon["ncbi_taxon_id"],
                            species=taxon["species"],
                            web=web,
                            data=raw["data"],
                            status=StatusMessage.DATA_SUCCESS.value,
                            info=InfoMessage.DATA_RETRIEVED.value,
                        )
                    )
                found_webs.add(web)

        # Handle missing webs
        missing_webs = set(web_for_query) - found_webs
        for web in missing_webs:
            result.append(
                RawDeleteResponseModelObject(
                    taxon_id=taxon["taxon_id"],
                    ncbi_taxon_id=taxon["ncbi_taxon_id"],
                    species=taxon["species"],
                    web=web,
                    data=None,
                    status=StatusMessage.DATA_FAILED.value,
                    info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.RAW_NOT_EXIST.value}",
                )
            )

    # Append not found taxa
    result.extend(
        [
            RawDeleteResponseModelObject(
                ncbi_taxon_id=ncbi_id,
                species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                web=None,
                data=None,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}",
            )
            for ncbi_id in not_found_taxa
        ]
    )

    # Append taxa with no portal
    result.extend(
        [
            RawDeleteResponseModelObject(
                taxon_id=taxon["taxon_id"],
                ncbi_taxon_id=taxon["ncbi_taxon_id"],
                species=taxon["species"],
                web=None,
                data=None,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",
            )
            for taxon in taxa_with_no_portal
        ]
    )

    return result
