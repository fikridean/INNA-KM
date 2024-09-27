from typing import List
from fastapi import HTTPException
import httpx

from config import OPERATIONS_FOLDERS
from models.portal_model import PortalBaseModel, PortalDeleteModel, PortalDetailModel, PortalGetModel, PortalRetrieveDataModel
from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import get_portals_webs, run_function_from_module

from database.mongo import client, portal_collection

# Create portal in database
@log_function("Create portal")
async def create_portal(params: List[PortalBaseModel]) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                if not params:
                    raise HTTPException(status_code=400, detail="Input must be a non-empty array of objects.")
                
                portals_created: list = []
                
                for portal in params:
                    await portal_collection.update_one(
                        {
                            "species": portal.species,
                            "web": portal.web,
                        },
                        {"$set": {
                            "species": portal.species,
                            "web": portal.web,
                            "taxon_id": portal.taxon_id,
                        }},
                        upsert=True,
                        session=session
                    )

                    portals_created.append(f"{portal.species} ({portal.taxon_id}) - {portal.web}") 

                return portals_created

            except Exception as e:
                raise Exception(f"An error occurred while creating portal: {str(e)}")

# Delete portal from database
@log_function("Delete portal")
async def delete_portal(params: PortalDeleteModel) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                if not params.taxon_id or not params.web:
                    raise HTTPException(status_code=400, detail="For security reasons, you must provide both taxon_id and web.")
                
                portals_deleted: list = []
                
                if params.taxon_id and params.web:
                    portals = await portal_collection.find({
                        "taxon_id": {"$in": params.taxon_id},
                        "web": {"$in": params.web}
                    }, session=session).to_list(length=None)

                    if not portals:
                        raise HTTPException(status_code=404, detail="Portals not found.")

                    await portal_collection.delete_many(
                        {
                            "taxon_id": {"$in": params.taxon_id},
                            "web": {"$in": params.web}
                        },
                        session=session
                    )

                elif params.taxon_id and not params.web:
                    portals = await portal_collection.find({
                        "taxon_id": {"$in": params.taxon_id}
                    }, session=session).to_list(length=None)

                    if not portals:
                        raise HTTPException(status_code=404, detail="Portals not found.")

                    await portal_collection.delete_many(
                        {
                            "taxon_id": {"$in": params.taxon_id}
                        },
                        session=session
                    )

                elif params.web and not params.taxon_id:
                    portals = await portal_collection.find({
                        "web": {"$in": params.web}
                    }, session=session).to_list(length=None)

                    if not portals:
                        raise HTTPException(status_code=404, detail="Portals not found.")

                    await portal_collection.delete_many(
                        {
                            "web": {"$in": params.web}
                        },
                        session=session
                    )

                portals_deleted = [f"{portal['species']} ({portal['taxon_id']}) - {portal['web']}" for portal in portals]
                
                return portals_deleted
            except Exception as e:
                raise Exception(f"An error occurred while deleting portal: {str(e)}")

# Get portals from database
@log_function("Get portals")
async def get_portals(params: PortalGetModel) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                taxon_id_for_query = params.taxon_id
                web_for_query = params.web

                webs = [web[:-3] if web.endswith('.py') else web for web in get_portals_webs(OPERATIONS_FOLDERS)]

                if ((taxon_id_for_query == None or taxon_id_for_query == []) and (web_for_query == None or web_for_query == [])):
                    portals = await portal_collection.find({}, {'_id': 0}, session=session).to_list(length=None)
                    return portals
                
                elif ((taxon_id_for_query == None or taxon_id_for_query == []) and (web_for_query != None)):
                    portals = await portal_collection.find({'web': {'$in': web_for_query}}, {'_id': 0}, session=session).to_list(length=None)
                    return portals
                
                elif ((taxon_id_for_query != None) and (web_for_query == None or web_for_query == [])):
                    portals = await portal_collection.find(
                        {'taxon_id': {'$in': taxon_id_for_query}},
                        {'_id': 0},
                        session=session
                    ).to_list(length=None)
                
                else:
                    portals = await portal_collection.find({
                        'taxon_id': {'$in': taxon_id_for_query},
                        'web': {'$in': web_for_query}
                    }, {'_id': 0}, session=session).to_list(length=None)

                found_taxon_ids = {portal['taxon_id'] for portal in portals}

                not_found_taxon_ids = set(taxon_id_for_query) - found_taxon_ids

                result = {
                    'portals_found': {
                        'total_data': len(portals),
                        'data': portals
                    },
                    'portals_not_found': list(not_found_taxon_ids)
                }

                return result

            except Exception as e:
                raise Exception(f"An error occurred while retrieving portals: {str(e)}")

# Get detail portal from database
@log_function("Get portal detail")
async def get_portal_detail(params: PortalDetailModel) -> dict:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                portal = await portal_collection.find_one({
                    "taxon_id": params.taxon_id,
                    "web": params.web
                }, {'_id': 0}, session=session)

                if not portal:
                    raise HTTPException(status_code=404, detail="Portal not found.")
        
                return portal
            except Exception as e:
                raise Exception(f"An error occurred while retrieving portal detail: {str(e)}")

# Retrieve data from portal
@log_function("Retrieve data")
async def retrieve_data(params: PortalRetrieveDataModel) -> dict:
    try:
        portal = await portal_collection.find_one({
            "taxon_id": params.taxon_id,
            "web": params.web
        }, {'_id': 0})

        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        result = await run_function_from_module(portal['web'], "retrieve", portal)
        return result
    
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))