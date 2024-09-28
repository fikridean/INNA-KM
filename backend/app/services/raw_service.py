from fastapi import HTTPException
from config import OPERATIONS_FOLDERS
from models.portal_model import PortalRetrieveDataModel
from models.raw_model import RawBaseModel, RawDeleteModel, RawDeleteResponseModel, RawGetModel, RawGetResponseModel, RawStoreModel, RawStoreResponseModel
from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import get_portals_webs, run_function_from_module
from database.mongo import client, raw_collection
from .portal_service import get_portals, retrieve_data

# Get raw from raw collection
@log_function("Get raw from raw collection")
async def get_raw(params: RawGetModel) -> RawGetResponseModel:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                taxon_id_for_query = params.taxon_id
                web_for_query = params.web

                if ((taxon_id_for_query == None or taxon_id_for_query == []) and (web_for_query == None or web_for_query == [])):
                    raw = await raw_collection.find({}, {'_id': 0}, session=session).to_list(length=None)
                    return raw
                
                if ((taxon_id_for_query == None or taxon_id_for_query == []) and (web_for_query != None)):
                    raw = await raw_collection.find({'web': {'$in': web_for_query}}, {'_id': 0}, session=session).to_list(length=None)
                    return raw
                
                if ((taxon_id_for_query != None) and (web_for_query == None or web_for_query == [])):
                    raw = await raw_collection.find({'taxon_id': {'$in': taxon_id_for_query}}, {'_id': 0}, session=session).to_list(length=None)
                    return raw
                
                taxon_id_for_query = params.taxon_id
                web_for_query = params.web

                raw = await raw_collection.find({
                    'taxon_id': {'$in': taxon_id_for_query},
                    'web': {'$in': web_for_query}
                }, {'_id': 0}, session=session).to_list(length=None)

                return raw

            except Exception as e:
                raise Exception(f"An error occurred while retrieving raw: {str(e)}")
            
# Store raw to db with transaction
@log_function("Store raw to db with transaction")
async def store_raw_to_db(params: RawBaseModel):
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                for data in params:
                    await raw_collection.update_one({
                        'taxon_id': data['taxon_id'],
                        'web': data['web']
                    }, {"$set": data}, upsert=True, session=session)

            except Exception as e:
                raise Exception(f"An error occurred while storing raw: {str(e)}")
        
# Store raw from portals to raw collection
@log_function("Store raw from portals")
async def store_raw_from_portals(params: RawStoreModel) -> RawStoreResponseModel:
    try:
        taxon_id_for_query = params.taxon_id
        web_for_query = params.web

        # If no web is provided, get a default list of web sources
        if web_for_query:
            webs = web_for_query
        else:
            webs = get_portals_webs(OPERATIONS_FOLDERS)  # Fetch available web sources

        portals = await get_portals(params)

        taxon_with_no_portal = [taxon_id for taxon_id in taxon_id_for_query if taxon_id not in [portal['taxon_id'] for portal in portals]]
                        
        data_to_store = []
        found_taxon_web = {}

        # Loop through each portal to process and retrieve data
        for portal in portals:
            species_name = portal['species']
            taxon_id = portal['taxon_id']
            web_source = portal['web']
            
            paramsObj = {
                "taxon_id": taxon_id,
                "web": web_source
            }

            params = PortalRetrieveDataModel(**paramsObj)

            retrieved_data = await retrieve_data(params)

            # Initialize tracking for taxon_id if not already set
            if taxon_id not in found_taxon_web:
                found_taxon_web[taxon_id] = {
                    'species': species_name,  # Add species field
                    'found_webs': {
                        'exist': [],
                        'not_exist': []
                    },
                    'missing_webs': list(webs) 
                }

            # Check if retrieved data is found
            if retrieved_data:
                # Add the web source to the 'exist' list
                found_taxon_web[taxon_id]['found_webs']['exist'].append(web_source)

                # If data was found, remove the web from the missing list
                if web_source in found_taxon_web[taxon_id]['missing_webs']:
                    found_taxon_web[taxon_id]['missing_webs'].remove(web_source)

                # Prepare data to store
                data_to_store.append({
                    'web': portal['web'],
                    'species': portal['species'],
                    'taxon_id': portal['taxon_id'],
                    'data': await run_function_from_module(portal['web'], "data_processing", retrieved_data)
                })
            else:
                found_taxon_web[taxon_id]['found_webs']['not_exist'].append(web_source)

        # Store found data in the database
        await store_raw_to_db(data_to_store)

        # Create the result structure
        result = []

        for taxon_id, web_info in found_taxon_web.items():
            result.append({
                'taxon_id': taxon_id,
                'species': web_info['species'],
                'found_webs': web_info['found_webs'],
                'missing_webs': [web for web in web_info['missing_webs'] if web not in web_info['found_webs']['exist'] and web not in web_info['found_webs']['not_exist']]  # Filter missing_webs
            })

        for taxon_id in taxon_with_no_portal:
            result.append({
                'taxon_id': taxon_id,
                'species': 'Unknown species',
                'found_webs': {
                    'exist': [],
                    'not_exist': []
                },
                'missing_webs': list(webs)
            })

        return result


    except Exception as e:
        raise Exception(f"An error occurred while storing data from all portals: {str(e)}")

# Delete raw from raw collection
@log_function("Delete raw from raw collection")
async def delete_raw_from_db(params: RawDeleteModel) -> RawDeleteResponseModel:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                taxon_id_for_query = params.taxon_id
                web_for_query = params.web

                # If no web is provided, get a default list of web sources
                if web_for_query:
                    webs = web_for_query
                else:
                    webs = get_portals_webs(OPERATIONS_FOLDERS)  # Fetch available web sources

                portals = await get_portals(params)

                taxon_with_no_portal = [taxon_id for taxon_id in taxon_id_for_query if taxon_id not in [portal['taxon_id'] for portal in portals]]
                                
                found_taxon_web = {}

                # await raw_collection.delete_many({
                #     'taxon_id': {'$in': taxon_id_for_query},
                #     'web': {'$in': web_for_query}
                # }, session=session)

                # Loop through each portal to process and retrieve data
                for portal in portals:
                    species_name = portal['species']
                    taxon_id = portal['taxon_id']
                    web_source = portal['web']

                    # Initialize tracking for taxon_id if not already set
                    if taxon_id not in found_taxon_web:
                        found_taxon_web[taxon_id] = {
                            'species': species_name,  # Add species field
                            'found_webs': [],
                            'missing_webs': list(webs) 
                        }

                    # Add the web source to the list
                    found_taxon_web[taxon_id]['found_webs'].append(web_source)

                    # If data was found, remove the web from the missing list
                    if web_source in found_taxon_web[taxon_id]['missing_webs']:
                        found_taxon_web[taxon_id]['missing_webs'].remove(web_source)

                # Create the result structure
                result = []

                for taxon_id, web_info in found_taxon_web.items():
                    result.append({
                        'taxon_id': taxon_id,
                        'species': web_info['species'],
                        'found_webs': web_info['found_webs'],
                        'missing_webs': web_info['missing_webs']  # Filter missing_webs
                    })

                for taxon_id in taxon_with_no_portal:
                    result.append({
                        'taxon_id': taxon_id,
                        'species': 'Unknown species',
                        'found_webs': [],
                        'missing_webs': list(webs)
                    })

                return result

            except Exception as e:
                raise Exception(f"An error occurred while deleting raw: {str(e)}")