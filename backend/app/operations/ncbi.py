import asyncio
import httpx
import xmltodict
from utils.helper.func_helper import convert_to_string


# Get NCBI data
async def retrieve(taxon: dict) -> dict:
    # Get the NCBI taxon ID from the taxon data
    ncbi_taxon_id: str = taxon["ncbi_taxon_id"]

    # Construct a new URL to fetch data by the extracted ID
    url: str = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id={ncbi_taxon_id}"
    )

    # Initialize an empty dictionary for the data
    data: dict = {}

    # Create another asynchronous HTTP client session
    async with httpx.AsyncClient() as client:
        retry_count: int = 0
        while retry_count < 5:  # Retry the request up to 5 times if it fails
            try:
                # Send a GET request to the new URL
                response = await client.get(url)
                # Raise an exception if the request was unsuccessful
                response.raise_for_status()

                # Parse the XML response into a dictionary
                data = xmltodict.parse(response.text)
                break  # Break out of the loop if successful
            except httpx.HTTPError:
                # Retry after waiting for 20 seconds if unsuccessful
                await asyncio.sleep(20)
                retry_count += 1
                continue  # Retry if an error occurred

    # If using the taxon ID did not return any data, try using the species name
    if not data:
        # Get the species name from the taxon data
        taxon_species: str = taxon["species"]

        # Construct a new URL to fetch data by the extracted name
        url: str = (
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&term={taxon_species}"
        )

        # Create another asynchronous HTTP client session
        async with httpx.AsyncClient() as client:
            retry_count: int = 0
            while retry_count < 5:  # Retry the request up to 5 times if it fails
                try:
                    # Send a GET request to the new URL
                    response = await client.get(url)
                    # Raise an exception if the request was unsuccessful
                    response.raise_for_status()

                    # Parse the XML response into a dictionary
                    data = xmltodict.parse(response.text)
                    break  # Break out of the loop if successful
                except httpx.HTTPError:
                    # Retry after waiting for 20 seconds if unsuccessful
                    await asyncio.sleep(20)
                    retry_count += 1
                    continue  # Retry if an error occurred

        id: str = data["eSearchResult"]["IdList"]["Id"]

        # Construct a new URL to fetch data by the extracted ID
        url: str = (
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id={id}"
        )

        async with httpx.AsyncClient() as client:
            retry_count: int = 0
            while retry_count < 5:  # Retry the request up to 5 times if it fails
                try:
                    # Send a GET request to the new URL
                    response = await client.get(url)
                    # Raise an exception if the request was unsuccessful
                    response.raise_for_status()

                    # Parse the XML response into a dictionary
                    data = xmltodict.parse(response.text)
                    break  # Break out of the loop if successful
                except httpx.HTTPError:
                    # Retry after waiting for 20 seconds if unsuccessful
                    await asyncio.sleep(20)
                    retry_count += 1
                    continue  # Retry if an error occurred

    # Check if the data is empty
    if not data:
        return {}

    # Ensure the response contains the expected 'Taxon' data
    if not data["TaxaSet"]["Taxon"]:
        return {}

    # Extract the 'Taxon' data
    data = data["TaxaSet"]["Taxon"]

    # Return the parsed data
    return data


async def data_processing(retrieve_data) -> str:
    return convert_to_string(retrieve_data)
