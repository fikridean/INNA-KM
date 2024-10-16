from typing import List
from utils.helper.map_terms_helper import mapping
from utils.enum.status_code_enum import StatusCode
from utils.enum.message_enum import (
    ResponseMessage,
    SpeciesMessage,
    StatusMessage,
    InfoMessage,
)
from models.term_model import (
    TermDeleteModel,
    TermDeleteResponseModelObject,
    TermGetModel,
    TermGetResponseModelObject,
    TermStoreModel,
    TermStoreResponseModelObject,
    searchModel,
    searchResponseModelObject,
)
from utils.decorator.app_log_decorator import log_function
from database.mongo import (
    client,
    taxon_collection,
    term_collection,
    raw_collection,
    portal_collection,
)

from utils.helper.func_helper import find_matching_parts, portal_webs


# Store raw to terms documents
@log_function("Store raw to terms documents")
async def store_raw_to_terms(params: TermStoreModel) -> TermStoreResponseModelObject:
    # Validate input parameters
    if not params.taxon_id:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # Retrieve existing taxons from the collection
    existing_taxons: List[dict] = await taxon_collection.find(
        {"taxon_id": {"$in": params.taxon_id}}, {"_id": 0}
    ).to_list(length=None)

    existing_taxon_ids = {taxon["taxon_id"] for taxon in existing_taxons}
    not_existing_taxon_ids = set(params.taxon_id) - existing_taxon_ids

    result = []

    async with await client.start_session() as session:
        async with session.start_transaction():
            # Process existing taxons
            if existing_taxon_ids:
                portals = await portal_collection.find(
                    {"taxon_id": {"$in": list(existing_taxon_ids)}}, {"_id": 0}
                ).to_list(length=None)

                if not portals:
                    result.append(
                        TermStoreResponseModelObject(
                            taxon_id=None,
                            ncbi_taxon_id=None,
                            species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                            data=None,
                            status=StatusMessage.DATA_FAILED.value,
                            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}.",
                        )
                    )

                portal_map = {portal["taxon_id"]: portal for portal in portals}

                for taxon_id in existing_taxon_ids:
                    portal = portal_map.get(taxon_id)
                    taxon = next(
                        (
                            taxon
                            for taxon in existing_taxons
                            if taxon["taxon_id"] == taxon_id
                        ),
                        None,
                    )

                    if portal:
                        raws = await raw_collection.find(
                            {"portal_id": portal["portal_id"]}, {"_id": 0}
                        ).to_list(length=None)

                        mapped = mapping(raws)

                        data_to_store = {"taxon_id": taxon_id, "data": mapped}

                        await term_collection.update_one(
                            {"taxon_id": taxon_id}, {"$set": data_to_store}, upsert=True
                        )

                        result.append(
                            TermStoreResponseModelObject(
                                taxon_id=taxon_id,
                                ncbi_taxon_id=taxon["ncbi_taxon_id"],
                                species=taxon["species"],
                                data=mapped,
                                status=StatusMessage.DATA_SUCCESS.value,
                                info=f"{InfoMessage.DATA_RETRIEVED_AND_STORED.value}.",
                            )
                        )

            # Handle missing taxons
            for not_existing_taxon_id in not_existing_taxon_ids:
                result.append(
                    TermStoreResponseModelObject(
                        taxon_id=not_existing_taxon_id,
                        ncbi_taxon_id=None,
                        species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                        status=StatusMessage.DATA_FAILED.value,
                        info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}.",
                    )
                )

    return result


# Get terms data from database
@log_function("Get terms data")
async def get_terms(params: TermGetModel) -> TermGetResponseModelObject:
    async with await client.start_session() as session:
        async with session.start_transaction():
            # Retrieve existing taxons
            existing_taxons = await taxon_collection.find(
                {"ncbi_taxon_id": {"$in": params.ncbi_taxon_id}}, {"_id": 0}
            ).to_list(length=None)

            # Extract existing taxon and ncbi_taxon_ids
            existing_taxon_ids = [taxon["taxon_id"] for taxon in existing_taxons]
            existing_ncbi_taxon_ids = [
                taxon["ncbi_taxon_id"] for taxon in existing_taxons
            ]

            # Determine which ncbi_taxon_ids are missing
            not_existing_ncbi_taxon_ids = set(params.ncbi_taxon_id) - set(
                existing_ncbi_taxon_ids
            )

            result = []

            # Process existing taxons
            if existing_taxon_ids:
                portals = await portal_collection.find(
                    {"taxon_id": {"$in": existing_taxon_ids}}, {"_id": 0}
                ).to_list(length=None)

                if not portals:
                    result.append(
                        TermGetResponseModelObject(
                            taxon_id=None,
                            ncbi_taxon_id=None,
                            species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                            status=StatusMessage.DATA_FAILED.value,
                            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}.",
                        )
                    )

                portal_map = {portal["taxon_id"]: portal for portal in portals}
                taxon_map = {taxon["ncbi_taxon_id"]: taxon for taxon in existing_taxons}

                for ncbi_taxon_id in existing_ncbi_taxon_ids:
                    taxon = taxon_map.get(ncbi_taxon_id)
                    portal = portal_map.get(taxon["taxon_id"]) if taxon else None

                    if portal:
                        term = await term_collection.find_one(
                            {"taxon_id": portal["taxon_id"]}, {"_id": 0}
                        )

                        if term:
                            result.append(
                                TermGetResponseModelObject(
                                    taxon_id=term["taxon_id"],
                                    ncbi_taxon_id=ncbi_taxon_id,
                                    species=taxon["species"],
                                    data=term["data"],
                                    status=StatusMessage.DATA_FOUND.value,
                                    info=f"{InfoMessage.DATA_RETRIEVED.value}.",
                                )
                            )
                        else:
                            result.append(
                                TermGetResponseModelObject(
                                    taxon_id=portal["taxon_id"],
                                    ncbi_taxon_id=ncbi_taxon_id,
                                    species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                                    status=StatusMessage.DATA_FAILED.value,
                                    info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.RAW_NOT_EXIST.value}.",
                                )
                            )

            # Handle missing taxons
            for not_existing_ncbi_taxon_id in not_existing_ncbi_taxon_ids:
                result.append(
                    TermGetResponseModelObject(
                        taxon_id=None,
                        ncbi_taxon_id=not_existing_ncbi_taxon_id,
                        species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                        status=StatusMessage.DATA_FAILED.value,
                        info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}.",
                    )
                )

            return result


# Delete terms document
@log_function("Delete term document")
async def delete_term(params: TermDeleteModel) -> TermDeleteResponseModelObject:
    async with await client.start_session() as session:
        async with session.start_transaction():
            # Retrieve existing taxons
            existing_taxons = await taxon_collection.find(
                {"ncbi_taxon_id": {"$in": params.ncbi_taxon_id}}, {"_id": 0}
            ).to_list(length=None)

            # Extract existing taxon and ncbi_taxon_ids
            existing_taxon_ids = [taxon["taxon_id"] for taxon in existing_taxons]
            existing_ncbi_taxon_ids = [
                taxon["ncbi_taxon_id"] for taxon in existing_taxons
            ]

            # Determine which ncbi_taxon_ids are missing
            not_existing_ncbi_taxon_ids = set(params.ncbi_taxon_id) - set(
                existing_ncbi_taxon_ids
            )

            result = []

            # Process existing taxons
            if existing_taxon_ids:
                portals = await portal_collection.find(
                    {"taxon_id": {"$in": existing_taxon_ids}}, {"_id": 0}
                ).to_list(length=None)

                if not portals:
                    result.append(
                        TermDeleteResponseModelObject(
                            taxon_id=None,
                            ncbi_taxon_id=None,
                            species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                            status=StatusMessage.DATA_FAILED.value,
                            info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}.",
                        )
                    )

                portal_map = {portal["taxon_id"]: portal for portal in portals}
                taxon_map = {taxon["ncbi_taxon_id"]: taxon for taxon in existing_taxons}

                for ncbi_taxon_id in existing_ncbi_taxon_ids:
                    taxon = taxon_map.get(ncbi_taxon_id)
                    portal = portal_map.get(taxon["taxon_id"]) if taxon else None

                    if portal:
                        term = await term_collection.find_one(
                            {"taxon_id": portal["taxon_id"]}, {"_id": 0}
                        )

                        await term_collection.delete_one(
                            {"taxon_id": portal["taxon_id"]}
                        )

                        if term:
                            result.append(
                                TermDeleteResponseModelObject(
                                    taxon_id=term["taxon_id"],
                                    ncbi_taxon_id=ncbi_taxon_id,
                                    species=taxon["species"],
                                    data=term["data"],
                                    status=StatusMessage.DATA_SUCCESS.value,
                                    info=f"{InfoMessage.DATA_DELETED.value}.",
                                )
                            )
                        else:
                            result.append(
                                TermDeleteResponseModelObject(
                                    taxon_id=portal["taxon_id"],
                                    ncbi_taxon_id=ncbi_taxon_id,
                                    species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                                    status=StatusMessage.DATA_FAILED.value,
                                    info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.RAW_NOT_EXIST.value}.",
                                )
                            )

            # Handle missing taxons
            for not_existing_ncbi_taxon_id in not_existing_ncbi_taxon_ids:
                result.append(
                    TermGetResponseModelObject(
                        taxon_id=None,
                        ncbi_taxon_id=not_existing_ncbi_taxon_id,
                        species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                        status=StatusMessage.DATA_FAILED.value,
                        info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}.",
                    )
                )

            return result


# Search terms data from database
@log_function("Search terms data")
async def search_terms(params: searchModel) -> searchResponseModelObject:
    search_result = await term_collection.find(
        {"$text": {"$search": params.search}}, {"_id": 0, "taxon_id": 1, "data": 1}
    ).to_list(length=None)

    for item in search_result:
        taxon = await taxon_collection.find_one(
            {"taxon_id": item["taxon_id"]}, {"_id": 0, "species": 1}
        )

        item["species"] = taxon["species"]

    search_result_filtered = find_matching_parts(search_result, params.search)

    return search_result_filtered


# Create indexes
@log_function("Create indexes")
async def create_indexes() -> str:
    # Check if indexes already exist
    # indexes = await term_collection.index_information()

    # Create taxon_id index in taxon collection
    await taxon_collection.create_index(
        "taxon_id",
        name="taxon_id_index_taxa",
        unique=True,
    )

    # Create ncbi_taxon_id index in taxon collection
    await taxon_collection.create_index(
        "ncbi_taxon_id",
        name="ncbi_taxon_id_index_taxa",
        unique=True,
    )

    # Create taxon_id index in portal collection
    await portal_collection.create_index(
        "taxon_id",
        name="taxon_id_index_portal",
        unique=True,
    )

    # Create portal_id index in portal collection
    await portal_collection.create_index(
        "portal_id",
        name="portal_id_index_portal",
        unique=True,
    )

    # Create taxon_id index in term collection
    await term_collection.create_index(
        "taxon_id",
        name="taxon_id_index",
        unique=True,
    )

    # Create text index in term collection
    await term_collection.create_index(
        {"$**": "text"},
        name="search_index",
        language_override="none",
        default_language="en",
    )

    return "Indexes created successfully."
