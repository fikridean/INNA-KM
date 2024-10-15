from typing import Any, List, Set, Tuple, Dict
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
    RawBaseModel,
    RawDeleteModel,
    RawDeleteResponseModelObject,
    RawGetModel,
    RawGetResponseModelObject,
    RawStoreModel,
    RawStoreResponseModelObject,
)
from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import run_function_from_module, portal_webs
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
) -> List[
    RawStoreResponseModelObject
]:  # return type is List[RawStoreResponseModelObject]
    ncbi_taxon_id_for_query: List[str] = params.ncbi_taxon_id  # List of NCBI Taxon IDs
    web_for_query: List[str] = params.web or portal_webs  # List of web sources to query

    # Validate supported web sources
    unsupported_webs: List[str] = [
        web for web in web_for_query if web not in portal_webs
    ]  # List of unsupported webs
    if unsupported_webs:
        raise Exception(
            {
                "data": [],  # Empty list
                "message": f"Web sources not supported: {', '.join(unsupported_webs)}.",
                "status_code": StatusCode.BAD_REQUEST.value,  # Status code value
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
    taxa_not_found: set = set(ncbi_taxon_id_for_query) - {
        taxon["ncbi_taxon_id"] for taxon in taxa
    }  # Set of not found taxa

    # Prepare data structures
    data_to_store: List[dict] = []  # List of data to store
    found_taxon_web: dict = {  # Dictionary mapping taxon ID to details
        taxon["ncbi_taxon_id"]: {
            "species": taxon["species"],  # Species name
            "found_webs": {"exist": [], "not_exist": []},  # Found webs dictionary
            "missing_webs": set(web_for_query),  # Set of missing webs
            "status": StatusMessage.DATA_NOT_FOUND.value,  # Initial status message
            "info": InfoMessage.DATA_NOT_RETRIEVED_AND_STORED.value,  # Initial info message
        }
        for taxon in taxa
    }

    # Retrieve portals
    taxon_ids: List[str] = [taxon["taxon_id"] for taxon in taxa]  # List of taxon IDs
    portals: List[dict] = await portal_collection.find(
        {"taxon_id": {"$in": taxon_ids}},  # List of portal dictionaries
        {"_id": 0, "taxon_id": 1, "portal_id": 1, "web": 1},
    ).to_list(length=None)

    portal_map: dict = {
        portal["taxon_id"]: portal for portal in portals
    }  # Mapping of taxon_id to portal

    # Process each taxon
    for taxon in taxa:  # Iterating over each taxon
        portal: dict = portal_map.get(
            taxon["taxon_id"]
        )  # Portal dictionary for the taxon
        if portal:
            taxon["portal_id"] = portal["portal_id"]  # Assigning portal_id to taxon
            web_need_to_process: List[str] = filter_webs_for_processing(
                portal["web"], web_for_query
            )  # List of webs to process

            for web in web_need_to_process:  # Iterating over each web to process
                params: PortalRetrieveDataModel = PortalRetrieveDataModel(
                    ncbi_taxon_id=taxon["ncbi_taxon_id"], web=web
                )  # Model instance
                retrieved_data: PortalRetrieveDataResponseModelObject = (
                    await retrieve_data(params)
                )  # Retrieved data

                if retrieved_data:
                    retrieved_data = retrieved_data.data

                    found_taxon_web[taxon["ncbi_taxon_id"]]["found_webs"][
                        "exist"
                    ].append(
                        {
                            "web": web,
                            "status": StatusMessage.DATA_FOUND.value,  # Status message
                            "info": InfoMessage.DATA_RETRIEVED_AND_STORED.value,  # Info message
                        }
                    )
                    data_to_store.append(
                        {
                            "portal_id": taxon.get("portal_id"),  # Portal ID
                            "web": web,
                            "data": await run_function_from_module(
                                web, "data_processing", retrieved_data
                            ),  # Processed data
                        }
                    )
                else:
                    found_taxon_web[taxon["ncbi_taxon_id"]]["found_webs"][
                        "not_exist"
                    ].append(
                        {
                            "web": web,
                            "status": StatusMessage.DATA_NOT_FOUND.value,  # Status message
                            "info": InfoMessage.DATA_NOT_RETRIEVED_AND_STORED.value,  # Info message
                        }
                    )

                found_taxon_web[taxon["ncbi_taxon_id"]]["missing_webs"].discard(
                    web
                )  # Remove processed web

    async with await client.start_session() as session:  # session: AsyncIOMotorClient
        async with session.start_transaction():  # session: AsyncIOMotorSession
            for data in data_to_store:  # data: dict
                await raw_collection.update_one(
                    {
                        "portal_id": data["portal_id"],  # data['portal_id']: str
                        "web": data["web"],  # data['web']: str
                    },
                    {"$set": data},
                    upsert=True,
                    session=session,
                )

    # Prepare final result
    result: List[RawStoreResponseModelObject] = []  # List for final results
    for ncbi_taxon_id, details in found_taxon_web.items():  # Iterating over found taxa
        if not details["found_webs"]["exist"]:
            details["status"] = StatusMessage.DATA_FAILED.value  # Status update
            details["info"] = (
                InfoMessage.DATA_NOT_RETRIEVED_AND_STORED_FROM_ALL_WEB.value
            )  # Info update
        elif len(details["found_webs"]["exist"]) == len(web_for_query):
            details["status"] = StatusMessage.DATA_SUCCESS.value  # Status update
            details["info"] = (
                InfoMessage.DATA_RETRIEVED_AND_STORED_FROM_ALL_WEB.value
            )  # Info update

        result.append(
            RawStoreResponseModelObject(  # Creating a response model object
                ncbi_taxon_id=ncbi_taxon_id,  # NCBI Taxon ID
                species=details["species"],  # Species name
                found_webs=details["found_webs"],  # Found webs details
                missing_webs=list(details["missing_webs"]),  # Missing webs as a list
                status=details["status"],  # Status message
                info=details["info"],  # Info message
            )
        )

    result.extend(
        [
            RawStoreResponseModelObject(  # Extending results for not found taxa
                ncbi_taxon_id=ncbi_taxon_id,
                species=SpeciesMessage.SPECIES_NOT_FOUND.value,  # Species not found message
                found_webs={"exist": [], "not_exist": []},  # Empty found webs
                missing_webs=web_for_query.copy(),  # Copy of missing webs
                status=StatusMessage.DATA_FAILED.value,  # Status failed
                info=f"{InfoMessage.DATA_NOT_RETRIEVED_AND_STORED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",  # Info message
            )
            for ncbi_taxon_id in taxa_not_found
        ]
    )  # List comprehension for taxa not found

    return result  # Return the result list


# Get raw from raw collection
@log_function("Get raw from raw collection")
async def get_raw(params: RawGetModel) -> List[RawGetResponseModelObject]:
    query_ncbi_taxon_id: Dict[str, Any] = (
        {"ncbi_taxon_id": {"$in": params.ncbi_taxon_id}} if params.ncbi_taxon_id else {}
    )
    web_for_query: List[str] = params.web or portal_webs

    taxa: List[Dict[str, Any]] = await taxon_collection.find(
        query_ncbi_taxon_id, {"_id": 0}
    ).to_list(length=None)
    ncbi_taxon_ids: List[str] = [taxon["ncbi_taxon_id"] for taxon in taxa]
    taxon_ids: List[str] = [taxon["taxon_id"] for taxon in taxa]

    not_found_taxa: List[str] = [
        ncbi_taxon_id
        for ncbi_taxon_id in params.ncbi_taxon_id
        if ncbi_taxon_id not in ncbi_taxon_ids
    ]

    portals: List[Dict[str, Any]] = await portal_collection.find(
        {"taxon_id": {"$in": taxon_ids}}, {"_id": 0}
    ).to_list(length=None)
    portal_map: Dict[str, str] = {
        portal["taxon_id"]: portal["portal_id"] for portal in portals
    }

    for taxon in taxa:
        taxon["portal_id"] = portal_map.get(taxon["taxon_id"])

    result: List[RawGetResponseModelObject] = []
    portal_ids: List[str] = [
        taxon.get("portal_id") for taxon in taxa if "portal_id" in taxon
    ]

    raws: List[Dict[str, Any]] = await raw_collection.find(
        {"portal_id": {"$in": portal_ids}, "web": {"$in": web_for_query}}, {"_id": 0}
    ).to_list(length=None)

    raw_map: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for raw in raws:
        key: Tuple[str, str] = (raw["portal_id"], raw["web"])
        raw_map.setdefault(key, []).append(raw)

    for taxon in taxa:
        portal_id: str = taxon.get("portal_id")
        if not portal_id:
            continue

        found_webs: Set[str] = set()
        web_need_to_process: List[str] = filter_webs_for_processing(
            portal_webs, web_for_query
        )

        for web in web_need_to_process:
            raw_key: Tuple[str, str] = (portal_id, web)
            if raw_key in raw_map:
                for raw in raw_map[raw_key]:
                    result.append(
                        RawGetResponseModelObject(
                            ncbi_taxon_id=taxon["ncbi_taxon_id"],
                            species=taxon["species"],
                            web=web,
                            data=raw["data"],
                            status=StatusMessage.DATA_SUCCESS.value,
                            info=InfoMessage.DATA_RETRIEVED.value,
                        )
                    )
                found_webs.add(web)

        missing_webs: Set[str] = set(web_for_query) - found_webs

        for web in missing_webs:
            result.append(
                RawGetResponseModelObject(
                    ncbi_taxon_id=taxon["ncbi_taxon_id"],
                    species=taxon["species"],
                    web=web,
                    data=None,
                    status=StatusMessage.DATA_FAILED.value,
                    info=InfoMessage.DATA_NOT_RETRIEVED.value,
                )
            )

    # Append not found taxa
    result.extend(
        [
            RawGetResponseModelObject(
                ncbi_taxon_id=taxon_id,
                species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                web=None,
                data=None,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",
            )
            for taxon_id in not_found_taxa
        ]
    )

    return result


# Delete raw from raw collection
@log_function("Delete raw from raw collection")
async def delete_raw_from_db(
    params: RawDeleteModel,
) -> List[RawDeleteResponseModelObject]:
    query_ncbi_taxon_id: Dict[str, Any] = (
        {"ncbi_taxon_id": {"$in": params.ncbi_taxon_id}} if params.ncbi_taxon_id else {}
    )
    web_for_query: List[str] = params.web or portal_webs

    taxa: List[Dict[str, Any]] = await taxon_collection.find(
        query_ncbi_taxon_id, {"_id": 0}
    ).to_list(length=None)
    ncbi_taxon_ids: List[str] = [taxon["ncbi_taxon_id"] for taxon in taxa]
    taxon_ids: List[str] = [taxon["taxon_id"] for taxon in taxa]

    not_found_taxa: List[str] = [
        ncbi_taxon_id
        for ncbi_taxon_id in params.ncbi_taxon_id
        if ncbi_taxon_id not in ncbi_taxon_ids
    ]

    portals: List[Dict[str, Any]] = await portal_collection.find(
        {"taxon_id": {"$in": taxon_ids}}, {"_id": 0}
    ).to_list(length=None)
    portal_map: Dict[str, str] = {
        portal["taxon_id"]: portal["portal_id"] for portal in portals
    }

    for taxon in taxa:
        taxon["portal_id"] = portal_map.get(taxon["taxon_id"])

    result: List[RawDeleteResponseModelObject] = []
    portal_ids: List[str] = [
        taxon.get("portal_id") for taxon in taxa if "portal_id" in taxon
    ]

    raws: List[Dict[str, Any]] = await raw_collection.find(
        {"portal_id": {"$in": portal_ids}, "web": {"$in": web_for_query}}, {"_id": 0}
    ).to_list(length=None)

    raw_map: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for raw in raws:
        key: Tuple[str, str] = (raw["portal_id"], raw["web"])
        raw_map.setdefault(key, []).append(raw)

    for taxon in taxa:
        portal_id: str = taxon.get("portal_id")
        if not portal_id:
            continue

        found_webs: Set[str] = set()
        web_need_to_process: List[str] = filter_webs_for_processing(
            portal_webs, web_for_query
        )

        for web in web_need_to_process:
            raw_key: Tuple[str, str] = (portal_id, web)
            if raw_key in raw_map:
                for raw in raw_map[raw_key]:
                    result.append(
                        RawDeleteResponseModelObject(
                            ncbi_taxon_id=taxon["ncbi_taxon_id"],
                            species=taxon["species"],
                            web=web,
                            status=StatusMessage.DATA_SUCCESS.value,
                            info=InfoMessage.DATA_RETRIEVED.value,
                        )
                    )
                found_webs.add(web)

        missing_webs: Set[str] = set(web_for_query) - found_webs

        for web in missing_webs:
            result.append(
                RawDeleteResponseModelObject(
                    ncbi_taxon_id=taxon["ncbi_taxon_id"],
                    species=taxon["species"],
                    web=web,
                    status=StatusMessage.DATA_FAILED.value,
                    info=InfoMessage.DATA_NOT_RETRIEVED.value,
                )
            )

    # Append not found taxa
    result.extend(
        [
            RawDeleteResponseModelObject(
                ncbi_taxon_id=taxon_id,
                species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                web=None,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}",
            )
            for taxon_id in not_found_taxa
        ]
    )

    return result
