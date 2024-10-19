import asyncio
from bs4 import BeautifulSoup
import httpx
from config import BACDIVE_EMAIL, BACDIVE_PASSWORD
import bacdive
from utils.helper.func_helper import convert_to_string


# Get bacdive data
async def retrieve(taxon: dict) -> dict:
    # Get the taxon ID from the taxon data
    ncbi_taxon_id: str = taxon["ncbi_taxon_id"]

    bacdive_taxon_id: dict = {}

    # Send a request to BacDive search page using the taxon ID
    async with httpx.AsyncClient() as client:
        retry_count: int = 0
        while retry_count < 5:  # Retry the request up to 5 times if it fails
            try:
                # Send a GET request to BacDive search URL with NCBI taxon ID
                response = await client.get(
                    f"https://bacdive.dsmz.de/advsearch?fg%5B0%5D%5Bgc%5D=OR&fg%5B0%5D%5Bfl%5D%5B1%5D%5Bfd%5D=16S+associated+NCBI+tax+ID&fg%5B0%5D%5Bfl%5D%5B1%5D%5Bfo%5D=equal&fg%5B0%5D%5Bfl%5D%5B1%5D%5Bfv%5D={ncbi_taxon_id}&fg%5B0%5D%5Bfl%5D%5B1%5D%5Bfvd%5D=sequence_16S-tax_id-7"
                )
                # Raise an exception if the request was unsuccessful
                response.raise_for_status()

                # Parse the HTML response using BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")

                # Find all 'a' tags and extract the URLs from the href attributes
                links = soup.find_all("a")
                hrefs = [link.get("href") for link in links]

                # Extract the first strain URL and retrieve BacDive taxon ID
                first_strain_url = next(
                    (url for url in hrefs if url.startswith("/strain/")), None
                )

                if not first_strain_url:
                    return {}

                bacdive_taxon_id = first_strain_url.split("/")[-1]

                break  # Break out of the loop if successful

            except httpx.HTTPError:
                # Retry after waiting for 20 seconds if an error occurs
                print(f"Retrying after 20 seconds for {taxon['species']}")
                await asyncio.sleep(20)
                retry_count += 1
                continue  # Retry if unsuccessful

    if not bacdive_taxon_id:
        # Get the species name from the taxon data
        taxon_species: str = taxon["species"]

        bacdive_client = bacdive.BacdiveClient(BACDIVE_EMAIL, BACDIVE_PASSWORD)
        bacdive_client.search(taxonomy=taxon_species)

        # Return the retrieved data or an empty dict if no data is found
        if not bacdive_client.retrieve():
            return {}

        # Return the first result of the retrieved data
        return next(bacdive_client.retrieve())

    # Use BacDive client to search for data by BacDive taxon ID
    bacdive_client = bacdive.BacdiveClient(BACDIVE_EMAIL, BACDIVE_PASSWORD)
    query = {"id": bacdive_taxon_id}
    bacdive_client.search(**query)

    # Return the retrieved data or an empty dict if no data is found
    if not bacdive_client.retrieve():
        return {}

    # Return the first result of the retrieved data
    return next(bacdive_client.retrieve())


async def data_processing(retrieve_data: dict) -> str:
    return convert_to_string({str(k): v for k, v in retrieve_data.items()})
