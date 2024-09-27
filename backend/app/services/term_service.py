from typing import List
from fastapi import HTTPException
from models.term_model import TermStoreModel
from utils.helper.map_terms_helper import mapping
from utils.decorator.app_log_decorator import log_function
from database.mongo import client, terms_collection, raw_collection, portal_collection

from utils.helper.func_helper import find_matching_parts

# Get raw from raw collection based on only species with transaction
@log_function("Get raw from raw collection based on only species with transaction")
async def get_raw_based_only_taxon_id_with_transaction(params: List[TermStoreModel]) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                taxon_id_for_query = params.taxon_id

                if ((taxon_id_for_query == None or taxon_id_for_query == [])):
                    taxon_id_for_query = await portal_collection.distinct('taxon_id', session=session)

                raw_by_taxon_id = []

                for taxon_id in taxon_id_for_query:
                    raw = await raw_collection.find({
                        'taxon_id': taxon_id
                    }, {'_id': 0}).to_list(length=None)

                    raw_by_taxon_id.append(raw)

                return raw_by_taxon_id

            except Exception as e:
                raise Exception(f"An error occurred while retrieving raw: {str(e)}")
            
# Store raw to terms documents with transaction
@log_function("Store raw to terms documents with transaction")
async def store_raw_to_terms_with_transaction(params: list) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                for data in params:
                    await terms_collection.update_one({"taxon_id": data['taxon_id']}, {"$set": data}, upsert=True, session=session)

            except Exception as e:
                raise Exception(f"An error occurred while storing raw to terms documents: {str(e)}")

# Store raw to terms documents
@log_function("Store raw to terms documents")
async def store_raw_to_terms(params: List[TermStoreModel]) -> list:
    try:
        raws_by_taxon_id = await get_raw_based_only_taxon_id_with_transaction(params)

        combined_data_list = []

        for data in raws_by_taxon_id:
            mapped = await mapping(data)
            combined_data_list.append(mapped)

        await store_raw_to_terms_with_transaction(combined_data_list)

        return "Raw stored to terms documents successfully."

    except Exception as e:
        raise Exception(f"An error occurred while storing raw to terms documents: {str(e)}")

# Get terms data from database
@log_function("Get terms data")
async def get_terms(params: list) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:    
                species_for_query = params.species

                if ((species_for_query == None or species_for_query == [])):
                    terms = await raw_collection.find({}, {'_id': 0}, session=session).to_list(length=None)
                    return terms

                terms = await terms_collection.find({
                    'species': {'$in': species_for_query},
                }, {'_id': 0}, session=session ).to_list(length=1000)

                return terms

            except Exception as e:
                raise Exception(f"An error occurred while retrieving terms data: {str(e)}")
            
# Delete terms document
@log_function("Delete term document")
async def delete_term(params: list) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                species_for_query = params.species

                if ((species_for_query == None or species_for_query == [])):
                    await terms_collection.delete_many({}, session=session)
                    return "Terms documents deleted successfully."
                
                terms = await terms_collection.find({
                    'species': {'$in': species_for_query},
                }, session=session).to_list(length=None)

                if not terms:
                    raise HTTPException(status_code=404, detail="Terms not found.")

                await terms_collection.delete_many({
                    'species': {'$in': species_for_query},
                }, session=session)

                return "Terms documents deleted successfully."

            except Exception as e:
                raise Exception(f"An error occurred while deleting terms documents: {str(e)}")

# Store raw to term
@log_function("Store raw to term")
async def store_raw_to_term(params: list) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                species_for_query = params.species

                return species_for_query

            except Exception as e:
                raise Exception(f"An error occurred while storing raw to term: {str(e)}")

# Search terms data from database
@log_function("Search terms data")
async def search_terms(params: list) -> list:
    try:
        # indexes = await raw_collection.index_information()
        # print(indexes)

        # await raw_collection.create_index(
        #     { "$**": "text" },
        #     name='search_index',
        #     weights={
        #         "web": 10,
        #         "species": 10,
        #         "slug": 8,
        #         "data": 7
        #     },
        #     language_override='none',
        #     default_language='en',
        # )

        projection = {
            '_id': 0,
        }

        result = await raw_collection.find(
            { '$text': { '$search': params.search }},
            projection,
        ).to_list(1000)

        return find_matching_parts(result, params.search)
        
    except Exception as e:
        raise Exception(f"An error occurred while retrieving terms data: {str(e)}")