import asyncio
import httpx
from utils.helper.func_helper import convert_to_string


async def retrieve(taxon: dict) -> dict:
    # Construct the URL for GBIF species match API using the species name
    url: str = f'https://api.gbif.org/v1/species/match?name={taxon["species"]}'

    data: dict = {}

    async with httpx.AsyncClient() as client:
        retry_count: int = 0
        while retry_count < 5:  # Retry the request up to 5 times if it fails
            try:
                # Send a GET request to the GBIF species match API
                response = await client.get(url)
                # Raise an exception if the request was unsuccessful
                response.raise_for_status()

                # Parse the JSON response into a dictionary
                data = response.json()

                break  # Break out of the loop if successful

            except httpx.HTTPError:
                # Retry after waiting for 20 seconds if an error occurs
                await asyncio.sleep(20)
                retry_count += 1
                continue  # Retry if unsuccessful

    # Extract the usageKey from the data
    usage_key = data.get("usageKey")
    if not usage_key:
        return {}

    # Construct the URL for GBIF occurrence API using the usageKey
    url: str = f"https://api.gbif.org/v1/occurrence/search?taxonKey={usage_key}"

    async with httpx.AsyncClient() as client:
        retry_count: int = 0
        while retry_count < 5:  # Retry the request up to 5 times if it fails
            try:
                # Send a GET request to the GBIF occurrence API
                response = await client.get(url)
                # Raise an exception if the request was unsuccessful
                response.raise_for_status()

                # Parse the JSON response into a dictionary
                data = response.json()

                break  # Break out of the loop if successful

            except httpx.HTTPError:
                # Retry after waiting for 20 seconds if an error occurs
                await asyncio.sleep(20)
                retry_count += 1
                continue  # Retry if unsuccessful

    # Return the first result if available, otherwise return an empty dictionary
    if not data["results"][0]:
        return {}

    return data["results"][0]


async def data_processing(retrieve_data) -> str:
    return convert_to_string(retrieve_data)
