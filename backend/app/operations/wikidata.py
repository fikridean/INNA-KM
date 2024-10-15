import asyncio
import httpx
from utils.helper.func_helper import convert_to_string


async def retrieve(taxon: dict) -> dict:
    # Define the NCBI taxon ID property from Wikidata
    NCBI_TAXON_ID_CODE: str = "P685"

    # Get the NCBI taxon ID from the taxon data
    ncbi_taxon_id: str = taxon["ncbi_taxon_id"]

    # Construct the SPARQL query to fetch the item using the taxon ID
    query = f"""
        SELECT ?item WHERE {{
        ?item wdt:{NCBI_TAXON_ID_CODE} "{ncbi_taxon_id}".
        }}
    """

    # Define the request headers for the SPARQL query
    headers: dict = {"Accept": "application/sparql-results+json"}

    # Initialize an empty dictionary for the data
    data: dict = {}

    # Define the Wikidata SPARQL endpoint URL
    WIKIDATA_SPARQL_URL: str = "https://query.wikidata.org/sparql"

    # Send the SPARQL query using an asynchronous HTTP client
    async with httpx.AsyncClient() as client:
        retry_count: int = 0
        while retry_count < 5:  # Retry the request up to 5 times
            try:
                # Send GET request to Wikidata SPARQL endpoint
                response = await client.get(
                    WIKIDATA_SPARQL_URL, params={"query": query}, headers=headers
                )
                response.raise_for_status()  # Raise exception if the response status is an error

                # Parse the response JSON if successful
                data = response.json()
                break  # Exit the loop if the request was successful
            except httpx.HTTPError:
                # If the request fails, wait for 20 seconds and retry
                await asyncio.sleep(20)
                retry_count += 1
                continue  # Retry if an error occurred

    # If using the taxon ID did not return any data, try using the species name
    if not data:
        # Get the species name from the taxon data
        taxon_species: str = taxon["species"]

        # Construct the SPARQL query to fetch the item using the species name
        query = f"""
            SELECT ?item WHERE {{
                ?item rdfs:label "{taxon_species}"@en.
            }}
        """

        # Send the SPARQL query using an asynchronous HTTP client
        async with httpx.AsyncClient() as client:
            retry_count: int = 0
            while retry_count < 5:  # Retry the request up to 5 times
                try:
                    # Send GET request to Wikidata SPARQL endpoint
                    response = await client.get(
                        WIKIDATA_SPARQL_URL, params={"query": query}, headers=headers
                    )
                    response.raise_for_status()  # Raise exception if the response status is an error

                    # Parse the response JSON if successful
                    data = response.json()
                    break  # Exit the loop if the request was successful
                except httpx.HTTPError:
                    # If the request fails, wait for 20 seconds and retry
                    await asyncio.sleep(20)
                    retry_count += 1
                    continue  # Retry if an error occurred

    # If no data was returned, return an empty dictionary
    if not data:
        return {}

    # Check if the response contains any results, return an empty dictionary if not
    if not data["results"]["bindings"]:
        return {}

    # Extract the entity ID from the query results
    id: str = data["results"]["bindings"][0]["item"]["value"].split("/")[-1]

    # Return an empty dictionary if the ID is empty
    if not id:
        return {}

    # Construct the URL to fetch detailed data for the entity using its ID
    url: str = (
        f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={id}&languages=en"
    )

    # Send a GET request to the Wikidata API to retrieve the entity data
    async with httpx.AsyncClient() as client:
        retry_count: int = 0
        while retry_count < 5:  # Retry up to 5 times if the request fails
            try:
                # Send GET request to Wikidata API to fetch the entity details
                response = await client.get(url)
                response.raise_for_status()  # Raise exception if the response status is an error

                # Parse the response as JSON
                data = response.json()
                break  # Exit the loop if the request was successful

            except httpx.HTTPError:
                await asyncio.sleep(20)
                retry_count += 1
                continue  # Retry the request

    # If no data was returned, return an empty dictionary
    if not data:
        return {}

    # If the entity is not found in the response, return an empty dictionary
    if not data["entities"][id]:
        return {}

    # Return the data fetched from Wikidata
    return data["entities"][id]


async def data_processing(retrieve_data) -> str:
    return convert_to_string(retrieve_data)
