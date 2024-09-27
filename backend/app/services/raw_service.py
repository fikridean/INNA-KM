from fastapi import HTTPException
from models.portal_model import PortalRetrieveDataModel
from models.raw_model import RawBaseModel, RawDeleteModel, RawGetModel, RawStoreModel
from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import run_function_from_module
from database.mongo import client, raw_collection
from .portal_service import get_portals, retrieve_data

# Get raw from raw collection
@log_function("Get raw from raw collection")
async def get_raw(params: RawGetModel) -> list:
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
async def store_raw_to_db(params: RawBaseModel) -> str:
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
async def store_raw_from_portals(params: RawStoreModel) -> str:
    try:
        portals = await get_portals(params)

        if not portals:
            raise HTTPException(status_code=404, detail="Portal not found. Please re-check the taxon_id and web.")
        
        data_to_store = []
        data_exist = []
        data_not_exist = []

        for portal in portals:
            print(portal)
            paramsObj = {
                "taxon_id": portal['taxon_id'],
                "web": portal['web']
            }

            params = PortalRetrieveDataModel(**paramsObj)

            retrieved_data = await retrieve_data(params)

            if not retrieved_data:
                data_not_exist.append(f"{portal['species']} ({portal['taxon_id']}) - {portal['web']}")
            else:
                data_exist.append(f"{portal['species']} ({portal['taxon_id']}) - {portal['web']}")

            data = {
                'web': portal['web'],
                'species': portal['species'],
                'taxon_id': portal['taxon_id'],
                'data': await run_function_from_module(portal['web'], "data_processing", retrieved_data)
            }

            data_to_store.append(data)

        await store_raw_to_db(data_to_store)

        return {
            "total_portal_found": len(portals),
            "data_stored": {
                "total_data": len(data_exist),
                "data": data_exist
            },
            "data_not_stored": {
                "total_data": len(data_not_exist),
                "data": data_not_exist,
                "note": "Data not exist means the data cannot be retrieved from the portal and the species term data (data without the retrieved data from website) is still stored in the raw collection."
            }
        }

    except Exception as e:
        raise Exception(f"An error occurred while storing data from all portals: {str(e)}")

# Delete raw from raw collection
@log_function("Delete raw from raw collection")
async def delete_raw_from_db(params: RawDeleteModel) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                taxon_id_for_query = params.taxon_id
                web_for_query = params.web

                raws = await raw_collection.find({
                    'taxon_id': {'$in': taxon_id_for_query},
                    'web': {'$in': web_for_query}
                }, {'_id': 0}, session=session).to_list(length=None)

                if not raws:
                    raise HTTPException(status_code=404, detail="Raw not found. Please re-check the taxon_id and web.")

                await raw_collection.delete_many({
                    'taxon_id': {'$in': taxon_id_for_query},
                    'web': {'$in': web_for_query}
                }, session=session)
                
                raws_deleted = [f"{raw['species']} ({raw['taxon_id']}) - {raw['web']}" for raw in raws]

                return {
                    "total_data": len(raws_deleted),
                    "data": raws_deleted
                }
            
            except Exception as e:
                raise Exception(f"An error occurred while deleting raw: {str(e)}")