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

                # Dictionary to hold portals grouped by species
                portals_by_species: dict = {}

                for portal in params:
                    species = portal.species
                    web = portal.web

                    # If the species is not already in the dictionary, add it
                    if species not in portals_by_species:
                        portals_by_species[species] = {
                            'taxon_id': portal.taxon_id,
                            'webs': []
                        }
                    
                    # Add the web details to the species entry without redundancy
                    portals_by_species[species]['webs'].append(web)

                    # Perform the database update operation
                    await portal_collection.update_one(
                        {
                            "species": species,
                            "web": web,
                        },
                        {"$set": {
                            "species": species,
                            "web": web,
                            "taxon_id": portal.taxon_id,
                        }},
                        upsert=True,
                        session=session
                    )

                result = [
                    {
                        'species': species,
                        'taxon_id': details['taxon_id'],
                        'webs': details['webs']
                    }
                    for species, details in portals_by_species.items()
                ]

                return result

            except Exception as e:
                raise Exception(f"An error occurred while creating portal: {str(e)}")
            
# Get Portal with detail
@log_function("Get portal with detail")
async def get_portals_with_detail(params: PortalGetModel) -> list:
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

                # Handle different cases of input
                if not taxon_id_for_query and not web_for_query:
                    # If both taxon_id and web are missing, return all portals
                    portals = await portal_collection.find({}, {'_id': 0}, session=session).to_list(length=None)
                    return portals

                elif not taxon_id_for_query and web_for_query:
                    # If taxon_id is missing but web is provided, return portals with matching web
                    portals = await portal_collection.find({'web': {'$in': web_for_query}}, {'_id': 0}, session=session).to_list(length=None)
                    return portals

                elif taxon_id_for_query and not web_for_query:
                    # If web is missing but taxon_id is provided, return portals with matching taxon_id
                    portals = await portal_collection.find({'taxon_id': {'$in': taxon_id_for_query}}, {'_id': 0}, session=session).to_list(length=None)

                else:
                    # If both taxon_id and web are provided
                    portals = await portal_collection.find({
                        'taxon_id': {'$in': taxon_id_for_query},
                        'web': {'$in': web_for_query}
                    }, {'_id': 0}, session=session).to_list(length=None)

                # Track found and missing taxon_id and web pairs
                found_taxon_web = {}

                for portal in portals:
                    taxon_id = portal['taxon_id']
                    web_source = portal['web']
                    species_name = portal.get('species', 'Unknown species')  # Get species name or default to 'Unknown species'

                    if taxon_id not in found_taxon_web:
                        # Initialize the taxon entry with found and missing webs
                        found_taxon_web[taxon_id] = {
                            'species': species_name,  # Add species field
                            'found_webs': [],
                            'missing_webs': list(webs)  # Initially, assume all webs are missing
                        }

                    # Add the web source to the found list
                    found_taxon_web[taxon_id]['found_webs'].append(web_source)
                    
                    # Remove the web source from the missing list
                    if web_source in found_taxon_web[taxon_id]['missing_webs']:
                        found_taxon_web[taxon_id]['missing_webs'].remove(web_source)

                # Handle cases where taxon_id was provided but no portals were found
                for taxon_id in taxon_id_for_query:
                    if taxon_id not in found_taxon_web:
                        # This taxon_id was not found in the portals, so mark all webs as missing
                        found_taxon_web[taxon_id] = {
                            'species': 'Unknown species',  # In case the species isn't found
                            'found_webs': [],
                            'missing_webs': list(webs)  # All webs are missing since no portals found
                        }

                # Create the result structure
                result = [
                    {
                        'taxon_id': taxon_id,
                        'species': found_taxon_web[taxon_id]['species'],  # Include the species name
                        'found_webs': found_taxon_web[taxon_id]['found_webs'],
                        'missing_webs': found_taxon_web[taxon_id]['missing_webs']
                    }
                    for taxon_id in found_taxon_web
                ]
              
                return result

            except Exception as e:
                raise Exception(f"An error occurred while retrieving portals: {str(e)}")

            
# Get portals from database
@log_function("Get portals")
async def get_portals(params: PortalGetModel) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                taxon_id_for_query = params.taxon_id
                web_for_query = params.web

                # Handle different cases of input
                if not taxon_id_for_query and not web_for_query:
                    # If both taxon_id and web are missing, return all portals
                    portals = await portal_collection.find({}, {'_id': 0}, session=session).to_list(length=None)
                    return portals

                elif not taxon_id_for_query and web_for_query:
                    # If taxon_id is missing but web is provided, return portals with matching web
                    portals = await portal_collection.find({'web': {'$in': web_for_query}}, {'_id': 0}, session=session).to_list(length=None)
                    return portals

                elif taxon_id_for_query and not web_for_query:
                    # If web is missing but taxon_id is provided, return portals with matching taxon_id
                    portals = await portal_collection.find({'taxon_id': {'$in': taxon_id_for_query}}, {'_id': 0}, session=session).to_list(length=None)

                else:
                    # If both taxon_id and web are provided
                    portals = await portal_collection.find({
                        'taxon_id': {'$in': taxon_id_for_query},
                        'web': {'$in': web_for_query}
                    }, {'_id': 0}, session=session).to_list(length=None)

                return portals


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

# Delete portal from database
@log_function("Delete portal")
async def delete_portal(params: PortalDeleteModel) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                # Ensure both taxon_id and web are provided
                if not params.taxon_id or not params.web:
                    raise HTTPException(status_code=400, detail="For security reasons, you must provide both taxon_id and web.")
                
                taxon_id_for_query = params.taxon_id
                web_for_query = params.web
                
                # Find portals that match the query before deletion
                portals = await portal_collection.find({
                    "taxon_id": {"$in": taxon_id_for_query},
                    "web": {"$in": web_for_query}
                }, {'_id': 0}, session=session).to_list(length=None)
                
                # Delete portals that match the query
                await portal_collection.delete_many(
                    {
                        "taxon_id": {"$in": taxon_id_for_query},
                        "web": {"$in": web_for_query}
                    },
                    session=session
                )

                # Track found taxon IDs and web sources
                found_taxon_web = {}
                for portal in portals:
                    taxon_id = portal['taxon_id']
                    web_source = portal['web']

                    if taxon_id not in found_taxon_web:
                        found_taxon_web[taxon_id] = {'found_webs': [], 'missing_webs': list(web_for_query), 'portal': portal}

                    found_taxon_web[taxon_id]['found_webs'].append(web_source)

                    # Remove found webs from missing_webs
                    if web_source in found_taxon_web[taxon_id]['missing_webs']:
                        found_taxon_web[taxon_id]['missing_webs'].remove(web_source)

                # Handle taxon IDs not found in the portals
                for taxon_id in taxon_id_for_query:
                    if taxon_id not in found_taxon_web:
                        found_taxon_web[taxon_id] = {
                            'found_webs': [],
                            'missing_webs': list(web_for_query),  # All webs are missing
                            'portal': None  # No portal found for this taxon_id
                        }

                # Structure the result
                result = {
                    'total_data': len(found_taxon_web),
                    'data': [
                        {
                            'taxon_id': taxon_id,
                            'found_webs': found_taxon_web[taxon_id]['found_webs'],
                            'missing_webs': found_taxon_web[taxon_id]['missing_webs'],
                        }
                        for taxon_id in found_taxon_web
                    ]
                }

                return result
            
            except Exception as e:
                raise Exception(f"An error occurred while deleting portal: {str(e)}")


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