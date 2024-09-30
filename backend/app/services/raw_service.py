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
                
                elif ((taxon_id_for_query == None or taxon_id_for_query == []) and (web_for_query != None)):
                    raw = await raw_collection.find({'web': {'$in': web_for_query}}, {'_id': 0}, session=session).to_list(length=None)
                
                elif ((taxon_id_for_query != None) and (web_for_query == None or web_for_query == [])):
                    raw = await raw_collection.find({'taxon_id': {'$in': taxon_id_for_query}}, {'_id': 0}, session=session).to_list(length=None)

                else:
                    raw = await raw_collection.find({
                        'taxon_id': {'$in': taxon_id_for_query},
                        'web': {'$in': web_for_query}
                    }, {'_id': 0}, session=session).to_list(length=None)

                return raw

            except Exception as e:
                raise Exception(f"An error occurred while retrieving raw: {str(e)}")
            
# Get raw with web detail
@log_function("Get raw with web detail")
async def get_raw_with_web_detail(params: RawGetModel) -> RawGetResponseModel:
    try:
        raws = await get_raw(params)
        
        taxon_id_for_query = params.taxon_id
        web_for_query = params.web

        # If no web is provided, get a default list of web sources
        if not web_for_query:
            web_for_query = [web.split(".")[0] for web in get_portals_webs(OPERATIONS_FOLDERS)]

        # Get taxon id with no data
        taxon_with_no_data = [taxon_id for taxon_id in taxon_id_for_query if taxon_id not in [raw['taxon_id'] for raw in raws]]

        # Track found and missing taxon_id and web pairs
        found_taxon_web = {}
    
        # Loop through the raws to build the result
        for raw in raws:
            taxon_id = raw['taxon_id']
            web_source = raw['web']

            if taxon_id not in found_taxon_web:
                found_taxon_web[taxon_id] = {
                    'species': raw.get('species', 'Unknown species'),  # Add species field
                    'found_webs': {},
                    'missing_webs': list(web_for_query),  # Initialize with all provided web sources
                    'status': 'not_found',
                    'info': 'No data found for any provided web sources.',
                }

            if web_source not in found_taxon_web[taxon_id]['found_webs']:
                found_taxon_web[taxon_id]['found_webs'][web_source] = {
                    'status': 'found',
                    'info': 'Data found',
                    'data': raw.get('data', {})
                }

            # Remove found webs from missing_webs
            if web_source in found_taxon_web[taxon_id]['missing_webs']:
                found_taxon_web[taxon_id]['missing_webs'].remove(web_source)

            # Update status and info
            found_taxon_web[taxon_id]['status'] = 'partially_found'
            found_taxon_web[taxon_id]['info'] = 'Data found for some webs.'

        result = []

        # Loop through the found_taxon_web to build the result
        for taxon_id, details in found_taxon_web.items():

            if not details['found_webs']:
                details['status'] = 'not_found'
                details['info'] = 'No data found for any provided web sources.'
            elif len(details['found_webs']) == len(web_for_query):
                details['status'] = 'found'
                details['info'] = 'Data found for all provided web sources.'

            result.append({
                'taxon_id': taxon_id,
                'species': details['species'],
                'found_webs': details['found_webs'],
                'missing_webs': details['missing_webs'],
                'status': details['status'],
                'info': details['info']
            })

        # Handle taxon IDs not found in the raws
        for taxon_id in taxon_with_no_data:
            result.append({
                'taxon_id': taxon_id,
                'species': 'Unknown species',
                'found_webs': {},
                'missing_webs': web_for_query.copy(),
                'status': 'not_found',
                'info': 'No data found for any provided web sources.'
            })

        return result

    except Exception as e:
        raise Exception(f"An error occurred while retrieving raw with web detail: {str(e)}")
            
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
        if not web_for_query:
            web_for_query = [web.split(".")[0] for web in get_portals_webs(OPERATIONS_FOLDERS)]

        # Retrieve available portals for the provided taxon IDs
        portals = await get_portals(params)

        # Find taxon IDs that don't have corresponding portals
        taxon_with_no_portal = [taxon_id for taxon_id in taxon_id_for_query if taxon_id not in [portal['taxon_id'] for portal in portals]]

        # Prepare to store processed data and track which taxon_id and web combinations were found
        data_to_store = []
        found_taxon_web = {}

        # Loop through each portal to process and retrieve data
        for portal in portals:
            species_name = portal['species']
            taxon_id = portal['taxon_id']
            web_source = portal['web']
            
            # Define parameters for data retrieval
            paramsObj = {
                "taxon_id": taxon_id,
                "web": web_source
            }

            params = PortalRetrieveDataModel(**paramsObj)

            # Retrieve data for the given taxon_id and web source
            retrieved_data = await retrieve_data(params)

            # Initialize tracking for taxon_id if not already set
            if taxon_id not in found_taxon_web:
                found_taxon_web[taxon_id] = {
                    'species': species_name,  # Add species field
                    'found_webs': {
                        'exist': [],
                        'not_exist': []
                    },
                    'missing_webs': list(web_for_query),  # Initialize with all webs to be checked,
                    'status': 'not_found',
                    'info': 'No data found for any provided web sources.',
                }

            # Check if data was retrieved successfully
            if retrieved_data:
                # Avoid duplicate entries in 'exist'
                if not any(web['web'] == web_source for web in found_taxon_web[taxon_id]['found_webs']['exist']):
                    found_taxon_web[taxon_id]['found_webs']['exist'].append({
                        'web': web_source,
                        'status': 'success',
                        'info': 'Data retrieved from source and stored successfully.',
                    })

                # If data was found, remove the web from the missing list
                if web_source in found_taxon_web[taxon_id]['missing_webs']:
                    found_taxon_web[taxon_id]['missing_webs'].remove(web_source)

                # Update status and info
                found_taxon_web[taxon_id]['status'] = 'partially_found'
                found_taxon_web[taxon_id]['info'] = 'Data retrieved from source and stored for some webs'

                # Process and store the data
                data_to_store.append({
                    'web': portal['web'],
                    'species': portal['species'],
                    'taxon_id': portal['taxon_id'],
                    'data': await run_function_from_module(portal['web'], "data_processing", retrieved_data)
                })
            else:
                # Avoid duplicate entries in 'not_exist'
                if not any(web['web'] == web_source for web in found_taxon_web[taxon_id]['found_webs']['not_exist']):
                    found_taxon_web[taxon_id]['found_webs']['not_exist'].append({
                        'web': web_source,
                        'status': 'not_found',
                        'info': 'No data retrieved from source and no data stored.',
                    })

                # If data was not found, remove the web from the missing list
                if web_source in found_taxon_web[taxon_id]['missing_webs']:
                    found_taxon_web[taxon_id]['missing_webs'].remove(web_source)

        # Store the processed data in the database
        await store_raw_to_db(data_to_store)

        # Prepare the final result structure
        result = []

        # Loop through the found_taxon_web to build the result
        for taxon_id, details in found_taxon_web.items():
            if not details['found_webs']:
                details['status'] = 'not_found'
                details['info'] = 'No data found for any provided web sources.'
            elif len(details['found_webs']['exist']) == len(web_for_query):
                details['status'] = 'found'
                details['info'] = 'Data retrieved from source and stored for all provided web sources.'

            result.append({
                'taxon_id': taxon_id,
                'species': details['species'],
                'found_webs': details['found_webs'],
                'missing_webs': details['missing_webs'],
                'status': details['status'],
                'info': details['info']
            })
            
        # Add taxon_ids that have no corresponding portal (not found)
        for taxon_id in taxon_with_no_portal:
            result.append({
                'taxon_id': taxon_id,
                'species': 'Unknown species',
                'found_webs': {
                    'exist': [],
                    'not_exist': []
                },
                'missing_webs': list(web_for_query),
                'status': 'not_found',
                'info': 'No portal found for this taxon_id.'
            })

        # Return the final result
        return result


    except Exception as e:
        raise Exception(f"An error occurred while storing data from all portals: {str(e)}")

# Delete raw from raw collection
@log_function("Delete raw from raw collection")
async def delete_raw_from_db(params: RawDeleteModel) -> RawDeleteResponseModel:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                # Ensure both taxon_id and web are provided
                if not params.taxon_id or not params.web:
                    raise HTTPException(status_code=400, detail="For security reasons, you must provide both taxon_id and web.")

                taxon_id_for_query = params.taxon_id
                web_for_query = params.web

                # If no web is provided, get a default list of web sources
                if not web_for_query:
                    web_for_query = [web.split(".")[0] for web in get_portals_webs(OPERATIONS_FOLDERS)]

                raws = await raw_collection.find({
                    'taxon_id': {'$in': taxon_id_for_query},
                    'web': {'$in': web_for_query}
                }, {'_id': 0}, session=session).to_list(length=None)

                await raw_collection.delete_many({
                    'taxon_id': {'$in': taxon_id_for_query},
                    'web': {'$in': web_for_query}
                }, session=session)

                # Track found taxon IDs and web sources
                found_taxon_web = {}
                for raw in raws:
                    taxon_id = raw['taxon_id']
                    web_source = raw['web']

                    if taxon_id not in found_taxon_web:
                        found_taxon_web[taxon_id] = {
                            'species': raw.get('species', 'Unknown species'),  # Add species field
                            'found_webs': [],
                            'missing_webs': list(web_for_query),  # Initialize with all provided web sources
                            'status': 'not_found',
                            'info': 'No data found for any provided web sources.',
                        }

                    # Avoid redundancy in 'exist' list
                    if web_source not in [entry['web'] for entry in found_taxon_web[taxon_id]['found_webs']]:
                        # Add web source to found webs
                        found_taxon_web[taxon_id]['found_webs'].append({
                            "web": web_source,
                            "status": "deleted",
                            "info": "Data deleted successfully."
                        })

                    # Remove found webs from missing_webs
                    if web_source in found_taxon_web[taxon_id]['missing_webs']:
                        found_taxon_web[taxon_id]['missing_webs'].remove(web_source)

                    # Update status and info
                    found_taxon_web[taxon_id]['status'] = 'partially_found'
                    found_taxon_web[taxon_id]['info'] = 'Data deleted for some web sources.'

                # Handle taxon IDs not found in the portals
                for taxon_id in taxon_id_for_query:
                    if taxon_id not in found_taxon_web:
                        found_taxon_web[taxon_id] = {
                            'species': 'Unknown species',  # In case the species isn't found
                            'found_webs': [],
                            'missing_webs': list(web_for_query),  # All webs are missing
                            'status': 'not_found',
                            'info': 'No data found for any provided web sources.',
                            'portal': None  # No portal found for this taxon_id
                        }

                # Update status to 'found' for taxon_ids where all webs are found
                for taxon_id, details in found_taxon_web.items():
                    if not details['found_webs']:
                        details['status'] = 'not_found'
                        details['info'] = 'No data found for any provided web sources.'
                    elif len(details['found_webs']) == len(web_for_query):
                        details['status'] = 'found'
                        details['info'] = 'Data deleted for all provided web sources.'

                # Structure the result
                result = [{
                            'taxon_id': taxon_id,
                            'species': found_taxon_web[taxon_id].get('species', 'Unknown species'),
                            'found_webs': found_taxon_web[taxon_id]['found_webs'],
                            'missing_webs': found_taxon_web[taxon_id]['missing_webs'],
                            'status': found_taxon_web[taxon_id]['status'],
                            'info': found_taxon_web[taxon_id]['info']
                        }
                        for taxon_id in found_taxon_web
                    ]

                return result

            except Exception as e:
                raise Exception(f"An error occurred while deleting raw: {str(e)}")