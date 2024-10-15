from typing import List
from fastapi import HTTPException
from utils.helper.map_terms_helper import mapping
from utils.enum.status_code_enum import StatusCode
from utils.enum.message_enum import ResponseMessage, SpeciesMessage, StatusMessage, InfoMessage
from models.term_model import TermDeleteModel, TermDeleteResponseModel, TermGetModel, TermGetResponseModel, TermGetResponseModelObject, TermStoreModel, TermStoreResponseModel, TermStoreResponseModelObject, searchModel, searchResponseModel
from utils.decorator.app_log_decorator import log_function
from database.mongo import client, taxon_collection, term_collection, raw_collection, portal_collection

from utils.helper.func_helper import find_matching_parts, portal_webs

# Store raw to terms documents
@log_function("Store raw to terms documents")
async def store_raw_to_terms(params: TermStoreModel) -> TermStoreResponseModelObject:
    # Validate input parameters
    if not params.taxon_id:
        raise Exception({
            "data": [],
            "message": ResponseMessage.INVALID_PAYLOAD.value,
            "status_code": StatusCode.BAD_REQUEST.value
        })

    # Retrieve existing taxons from the collection
    existing_taxons: List[dict] = await taxon_collection.find(
        {"taxon_id": {"$in": params.taxon_id}},
        {'_id': 0}
    ).to_list(length=None)

    existing_taxon_ids = {taxon['taxon_id'] for taxon in existing_taxons}
    not_existing_taxon_ids = set(params.taxon_id) - existing_taxon_ids

    result = []

    async with await client.start_session() as session:
        async with session.start_transaction():
            # Process existing taxons
            if existing_taxon_ids:
                portals = await portal_collection.find(
                    {"taxon_id": {"$in": list(existing_taxon_ids)}},
                    {'_id': 0}
                ).to_list(length=None)

                if not portals:
                    result.append(TermStoreResponseModelObject(
                        taxon_id=None,
                        ncbi_taxon_id=None,
                        species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                        status=StatusMessage.DATA_NOT_FOUND.value,
                        info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}."
                    ))
                
                portal_map = {portal['taxon_id']: portal for portal in portals}

                for taxon_id in existing_taxon_ids:
                    portal = portal_map.get(taxon_id)
                    if portal:
                        raws = await raw_collection.find(
                            {'portal_id': portal['portal_id']},
                            {'_id': 0}
                        ).to_list(length=None)

                        mapped = await mapping(raws)

                        data_to_store = {
                            "taxon_id": taxon_id,
                            "data": mapped
                        }

                        await term_collection.update_one(
                            {"taxon_id": taxon_id},
                            {"$set": data_to_store},
                            upsert=True
                        )

                        result.append(TermStoreResponseModelObject(
                            taxon_id=taxon_id,
                            data=mapped,
                            status=StatusMessage.DATA_SUCCESS.value,
                            info=f"{InfoMessage.DATA_RETRIEVED_AND_STORED.value}."
                        ))

            # Handle missing taxons
            for not_existing_taxon_id in not_existing_taxon_ids:
                result.append(TermStoreResponseModelObject(
                    taxon_id=not_existing_taxon_id,
                    ncbi_taxon_id=None,
                    species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                    status=StatusMessage.DATA_NOT_FOUND.value,
                    info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}."
                ))

    return result

# Get terms data from database
@log_function("Get terms data")
async def get_terms(params: TermGetModel) -> TermGetResponseModelObject:
    async with await client.start_session() as session:
        async with session.start_transaction():
            # Retrieve existing taxons
            existing_taxons = await taxon_collection.find(
                {"ncbi_taxon_id": {"$in": params.ncbi_taxon_id}},
                {'_id': 0}
            ).to_list(length=None)

            # Extract existing taxon and ncbi_taxon_ids
            existing_taxon_ids = [taxon['taxon_id'] for taxon in existing_taxons]
            existing_ncbi_taxon_ids = [taxon['ncbi_taxon_id'] for taxon in existing_taxons]
            
            # Determine which ncbi_taxon_ids are missing
            not_existing_ncbi_taxon_ids = set(params.ncbi_taxon_id) - set(existing_ncbi_taxon_ids)

            result = []

            # Process existing taxons
            if existing_taxon_ids:
                portals = await portal_collection.find(
                    {"taxon_id": {"$in": existing_taxon_ids}},
                    {'_id': 0}
                ).to_list(length=None)

                if not portals:
                    result.append(TermGetResponseModelObject(
                        taxon_id=None,
                        ncbi_taxon_id=None,
                        species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                        status=StatusMessage.DATA_NOT_FOUND.value,
                        info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.PORTAL_NOT_EXIST.value}."
                    ))

                portal_map = {portal['taxon_id']: portal for portal in portals}
                taxon_map = {taxon['ncbi_taxon_id']: taxon for taxon in existing_taxons}

                for ncbi_taxon_id in existing_ncbi_taxon_ids:
                    taxon = taxon_map.get(ncbi_taxon_id)
                    portal = portal_map.get(taxon['taxon_id']) if taxon else None

                    if portal:
                        term = await term_collection.find_one(
                            {"taxon_id": portal['taxon_id']},
                            {'_id': 0}
                        )

                        if term:
                            result.append(TermGetResponseModelObject(
                                taxon_id=term['taxon_id'],
                                ncbi_taxon_id=ncbi_taxon_id,
                                species=taxon['species'],
                                data=term['data'],
                                status=StatusMessage.DATA_FOUND.value,
                                info=f"{InfoMessage.DATA_RETRIEVED.value}."
                            ))
                        else:
                            result.append(TermGetResponseModelObject(
                                taxon_id=portal['taxon_id'],
                                ncbi_taxon_id=ncbi_taxon_id,
                                species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                                status=StatusMessage.DATA_NOT_FOUND.value,
                                info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.RAW_NOT_EXIST.value}."
                            ))

            # Handle missing taxons
            for not_existing_ncbi_taxon_id in not_existing_ncbi_taxon_ids:
                result.append(TermGetResponseModelObject(
                    taxon_id=None,
                    ncbi_taxon_id=not_existing_ncbi_taxon_id,
                    species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                    status=StatusMessage.DATA_NOT_FOUND.value,
                    info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}."
                ))

            return result



            



            
            
# Delete terms document
@log_function("Delete term document")
async def delete_term(params: TermDeleteModel) -> TermDeleteResponseModel:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                taxon_id_for_query = params.taxon_id

                if ((taxon_id_for_query == None or taxon_id_for_query == [])):
                    raise HTTPException(status_code=400, detail="For security reasons, you must provide taxon_id to delete terms.")
                
                terms = await term_collection.find({
                    'taxon_id': {'$in': taxon_id_for_query},
                }, session=session).to_list(length=None)

                await term_collection.delete_many({
                    'taxon_id': {'$in': taxon_id_for_query},
                }, session=session)

                taxon_with_no_data = [taxon_id for taxon_id in taxon_id_for_query if taxon_id not in [data['taxon_id'] for data in terms]]

                result = []

                for data in terms:
                    result.append({
                        "taxon_id": data['taxon_id'],
                        "species": data['species'],
                        "status": "found",
                        "info": "Data deleted successfully."
                    })

                for taxon_id in taxon_with_no_data:
                    result.append({
                        "taxon_id": taxon_id,
                        "species": "unknown species",
                        "status": "not_found",
                        "info": "No data found for this taxon_id."
                    })
                
                return result
            
            except Exception as e:
                raise Exception(f"An error occurred while deleting terms documents: {str(e)}")

# Search terms data from database
@log_function("Search terms data")
async def search_terms(params: searchModel) -> searchResponseModel:
    try:
        search_query = params.search

        projection = {
            '_id': 0,
        }

        result = await term_collection.find(
            { '$text': { '$search': search_query }},
            projection,
        ).to_list(1000)

        return find_matching_parts(result, search_query)
        
    except Exception as e:
        raise Exception(f"An error occurred while retrieving terms data: {str(e)}")
    
# Create indexes
@log_function("Create indexes")
async def create_indexes() -> str:
    try:
        indexes = await term_collection.index_information()

        await term_collection.create_index(
            { "$**": "text" },
            name='search_index',
            weights={
                "taxon_id": 10,
                "species": 8,
                "data": 6
            },
            language_override='none',
            default_language='en',
        )

        await term_collection.create_index(
            "taxon_id",
            name='taxon_id_index',
            unique=True,
        )

        await term_collection.create_index(
            "species",
            name='species_index',
        )

        return "Indexes created successfully."
    except Exception as e:
        raise Exception(f"An error occurred while creating indexes: {str(e)}")