from fastapi import HTTPException
from models.term_model import TermDeleteModel, TermGetModel, TermStoreModel
from utils.helper.map_terms_helper import mapping
from utils.decorator.app_log_decorator import log_function
from database.mongo import client, terms_collection, raw_collection, portal_collection

from utils.helper.func_helper import find_matching_parts

# Get raw from raw collection based on only taxon_id with transaction
@log_function("Get raw from raw collection based on only taxon_id with transaction")
async def get_raw_based_only_taxon_id_with_transaction(params: TermStoreModel) -> list:
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
                    
                    if not raw:
                        continue

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
async def store_raw_to_terms(params: TermStoreModel) -> list:
    try:
        taxon_id_for_query = params.taxon_id

        raws = await get_raw_based_only_taxon_id_with_transaction(params)

        combined_data_list = []
    
        for data in raws:
            mapped = await mapping(data)
            combined_data_list.append(mapped)

        await store_raw_to_terms_with_transaction(combined_data_list)

        taxon_with_no_raw_data = [taxon_id for taxon_id in taxon_id_for_query if taxon_id not in [data['taxon_id'] for data in combined_data_list]]

        result = []

        for data in combined_data_list:
            result.append({
                **data,
                "status": "found",
                "info:": "Data stored successfully."
            })

        for taxon_id in taxon_with_no_raw_data:
            result.append({
                "taxon_id": taxon_id,
                "species": "",
                "data": {},
                "status": "not_found",
                "info": "No data found for this taxon_id."
            })

        return result
    except Exception as e:
        raise Exception(f"An error occurred while storing raw to terms documents: {str(e)}")

# Get terms data from database
@log_function("Get terms data")
async def get_terms(params: TermGetModel) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:    
                taxon_id_for_query = params.taxon_id

                if ((taxon_id_for_query == None or taxon_id_for_query == [])):
                    terms = await raw_collection.find({}, {'_id': 0}, session=session).to_list(length=None)
                    return terms

                terms = await terms_collection.find({
                    'taxon_id': {'$in': taxon_id_for_query},
                }, {'_id': 0}, session=session ).to_list(length=1000)

                taxon_with_no_data = [taxon_id for taxon_id in taxon_id_for_query if taxon_id not in [data['taxon_id'] for data in terms]]

                result = []

                for data in terms:
                    result.append({
                        **data,
                        "status": "found",
                        "info": "Data retrieved successfully."
                    })

                for taxon_id in taxon_with_no_data:
                    result.append({
                        "taxon_id": taxon_id,
                        "species": "",
                        "data": {},
                        "status": "not_found",
                        "info": "No data found for this taxon_id."
                    })

                return result

            except Exception as e:
                raise Exception(f"An error occurred while retrieving terms data: {str(e)}")
            
# Delete terms document
@log_function("Delete term document")
async def delete_term(params: TermDeleteModel) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                taxon_id_for_query = params.taxon_id

                if ((taxon_id_for_query == None or taxon_id_for_query == [])):
                    raise HTTPException(status_code=400, detail="For security reasons, you must provide taxon_id to delete terms.")
                
                terms = await terms_collection.find({
                    'taxon_id': {'$in': taxon_id_for_query},
                }, session=session).to_list(length=None)

                await terms_collection.delete_many({
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
                        "species": "",
                        "status": "not_found",
                        "info": "No data found for this taxon_id."
                    })
                
                return result
            
            except Exception as e:
                raise Exception(f"An error occurred while deleting terms documents: {str(e)}")

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