# INNA Knowledge Management

This project is a **FastAPI-based web service** that aggregates, processes, and stores data from various external portals. Using **Motor**, an asynchronous MongoDB driver for Python, the service ensures efficient data management across multiple sources, consolidating information into a unified format ready for use in downstream applications.

## Project Overview

- **Type**: FastAPI-based web service
- **Database**: MongoDB, using **Motor** (an async MongoDB driver for Python)
- **Main Collections**:
  - `taxa`
  - `portals`
  - `raws`
  - `terms`

## Primary Objective

The primary goal of this project is to **aggregate data** from external portals (e.g., WikiData, NCBI, BacDive, GBIF), **clean** and **normalize** it, and **store** the consolidated information in a MongoDB database. This ensures that all data is processed efficiently and ready for use in various downstream applications.

## Architecture

- **FastAPI** for the web service framework, enabling high performance and easy-to-use APIs.
- **MongoDB** as the database, leveraging its flexibility in handling various types of data.
- **Motor** for asynchronous operations with MongoDB, ensuring non-blocking I/O and efficient performance for high-throughput tasks.

# Tutorial

Follow these steps to set up the project:

1. **Initialize a Git repository**:

   ```sh
   git init
   ```

2. **Add the remote repository**:

   ```sh
   git remote add origin https://github.com/fikridean/INNA-KM.git
   ```

3. **Fetch the latest changes from the remote repository**:

   ```sh
   git fetch
   ```

4. **Checkout the `dev` branch**:

   ```sh
   git checkout dev
   ```

5. **Navigate to the backend directory**:

   ```sh
   cd backend
   ```

6. **Copy the example environment file to create your own `.env` file**:
   ```sh
   cp app/.env.example app/.env
   ```

Make sure to fill in the necessary environment variables in the `.env` file before running the application.

- **Create a virtual environment**:

  ```sh
  python3 -m venv venv
  ```

- **Activate the virtual environment**:

  - For Linux/macOS:
    ```sh
    source venv/bin/activate
    ```
  - For Windows:
    ```sh
    venv\Scripts\activate
    ```

- **Install the required dependencies**:

  ```sh
  pip install -r requirements.txt
  ```

- **Run FastAPI**:

  ```sh
  fastapi dev app/main.py
  ```

- **Preview the documentation locally using MkDocs**:

  ```sh
  mkdocs serve
  ```

- **Setting up the Search feature**:
  For code to create the search index, please visit the [Search Index Section](/E/#setting-up-the-search-index).

For more information, please visit <a target=_blank href='https://github.com/fikridean/INNAKM'>INNAKM Github Repository</a>.

Follow these steps to set up the interface project:

1. **Navigate to the interface directory**:

   ```sh
   cd interface
   ```

2. **Build and run dockerized React app**:

   ```sh
   sudo docker build -t interface .
   ```

3. **Running the Docker container**:

   ```sh
   sudo docker run -p 3000:3000 interface
   ```

4. **Checkout the `dev` branch**:

   ```sh
   http://localhost:3000
   ```


# Portals & Species

## Types of portals

- <a href="https://www.wikidata.org/" target="_blank">WikiData</a>
- <a href="https://www.ncbi.nlm.nih.gov/" target="_blank">NCBI</a>
- <a href="https://bacdive.dsmz.de/" target="_blank">BacDive</a>
- <a href="https://www.gbif.org/" target="_blank">GBIF</a>

## Species

1. Achromobacter mucicolens
2. Aeromonas hydrophila
3. Chelatococcus thermostellatus
4. Cobetia marina
5. Dactylosporangium aurantiacum
6. Empedobacter tilapiae
7. Escherichia fergusonii
8. Klebsiella aerogenes
9. Klebsiella pasteurii
10. Klebsiella pneumoniae
11. Lactiplantibacillus plantarum
12. Luteibacter jiangsuensis
13. Myxococcus stipitatus
14. Ochrobactrum quorumnocens
15. Pantoea agglomerans
16. Pantoea dispersa
17. Pseudomonas ceruminis
18. Pseudomonas palmensis
19. Pseudomonas qingdaonensis
20. Raoultella ornithinolytica
21. Rhodopseudomonas palustris
22. Stenotrophomonas maltophilia
23. Streptomyces fagopyri
24. Streptomyces lutosisoli
25. Streptomyces mirabilis
26. Stutzerimonas stutzeri
27. Xanthomonas campestris
28. Rhizobium leguminosarum
29. Streptomyces kunmingensis
30. Streptomyces rochei
31. Streptomyces griseorubens
32. Streptomyces sp.
33. Streptomyces sampsonii
34. Micromonospora chalcea
35. Klebsiella quasuvaricola
36. Escherichia coli
37. Gulosibacter sp.
38. Pseudomonas hibiscicola
39. Providencia rettgeri
40. Burkholderia sp.
41. Klebsiella oxytoca
42. Brevibacterium ammoniilyticum
43. Escherichia sp.
44. Klebsiella quasipneumoniae
45. Klebsiella sp.
46. Pantoea
47. Pseudomonas sp.
48. Stenotrophomonas sp.
49. Xanthomonas sp.

**Total count: 49 species**

# Data Parsing

## Why is data parsing needed before adding data to the database?

Before inserting data into the database, it is crucial to follow the appropriate data parsing steps for each portal. Data parsing ensures that the data is correctly retrieved, processed, and transformed into the desired format before being stored.

## Wikidata

### Steps

1. **Define Variables**:

   - Set the constant `NCBI_TAXON_ID_CODE` to `"P685"`, representing the NCBI Taxon ID property from Wikidata.
   - Retrieve the NCBI Taxon ID (`ncbi_taxon_id`) from the provided `taxon` dictionary.

2. **Formulate SPARQL Query**:

   - Construct a SPARQL query to fetch the Wikidata entity based on the NCBI Taxon ID.

3. **Send SPARQL Query Request**:

   - Use `httpx.AsyncClient` to send an asynchronous GET request to the Wikidata SPARQL endpoint (`https://query.wikidata.org/sparql`) with the SPARQL query and proper headers.

4. **Retry Mechanism for SPARQL Query**:

   - Implement a retry mechanism that attempts to send the request up to 5 times in case of failure, with a 20-second delay between retries.

5. **Check for Empty Data**:

   - Check if the response contains valid data. If no data is returned, proceed to construct a new query using the species name.

6. **Query by Species Name (Fallback)**:

   - If the NCBI Taxon ID query returns no data, formulate a new SPARQL query to search for the species using the `taxon_species` field from the `taxon` dictionary.

7. **Send Species Query Request**:

   - Use `httpx.AsyncClient` again to send the species-based query to the Wikidata SPARQL endpoint, applying the same retry mechanism (up to 5 retries).

8. **Extract the Entity ID**:

   - After successfully receiving the response, extract the entity's ID from the `item` field in the query results. The ID is derived from the URL provided in the response.

9. **Check for Empty or Invalid ID**:

   - If no entity ID is found, return an empty dictionary to indicate no data was retrieved.

10. **Fetch Entity Data**:

    - Construct a URL (`https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={id}&languages=en`) using the extracted entity ID to retrieve detailed entity data from the Wikidata API.

11. **Retry Mechanism for Entity Data**:

    - Implement a retry mechanism similar to previous requests, retrying up to 5 times in case of HTTP errors, with a 20-second delay between attempts.

12. **Check for Empty Entity Data**:

    - If the API response contains no data or the `id` is not found in the `entities` field, return an empty dictionary.

13. **Return Final Data**:

    - If the entity data is successfully retrieved, return the entity data; otherwise, return an empty dictionary.

14. **Data Processing**:
    - Use the `convert_to_string()` function from `utils.helper.func_helper` to process the retrieved data and return it as a string.

### Codes

```python
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


```

## NCBI

### Steps

1. **Define Variables**:

   - Retrieve the `ncbi_taxon_id` and `species` from the provided taxon dictionary.

2. **Construct URL for Taxon ID**:

   - Build the URL to fetch data from NCBI using the extracted `ncbi_taxon_id`.

3. **Send GET Request for Taxon ID**:

   - Use `httpx.AsyncClient` to send a GET request to the NCBI API with the constructed URL.

4. **Retry Mechanism for Taxon ID Request**:

   - Implement a retry mechanism that attempts the request up to 5 times if it fails, with a 20-second delay between retries.

5. **Parse XML Response for Taxon ID**:

   - Convert the XML response from the NCBI API into a Python dictionary using `xmltodict`.

6. **Check for Empty Data from Taxon ID**:

   - Ensure the response contains valid data before proceeding. If no data is found, attempt to retrieve data using the species name.

7. **Construct URL for Species Name**:

   - Build a new URL to search for the taxon using the species name.

8. **Send GET Request for Species Name**:

   - Use `httpx.AsyncClient` to send a GET request to the NCBI API to search for the taxon by species name.

9. **Retry Mechanism for Species Name Request**:

   - Implement a retry mechanism that attempts the request up to 5 times if it fails, with a 20-second delay between retries.

10. **Parse XML Response for Species Name**:

    - Convert the XML response from the NCBI API into a Python dictionary using `xmltodict`.

11. **Extract Taxon ID from Search Results**:

    - Extract the taxon ID from the search results returned by the NCBI API.

12. **Construct URL to Fetch Taxon Data by ID**:

    - Build another URL to fetch the detailed taxon data using the extracted ID.

13. **Send GET Request to Fetch Taxon Data**:

    - Use `httpx.AsyncClient` to send a GET request to the NCBI API using the new URL.

14. **Retry Mechanism for Fetching Taxon Data**:

    - Implement a retry mechanism that attempts the request up to 5 times if it fails, with a 20-second delay between retries.

15. **Parse Final XML Response**:

    - Convert the final XML response into a Python dictionary using `xmltodict`.

16. **Check for Final Data Validity**:

    - Ensure the response contains valid 'Taxon' data before proceeding.

17. **Return Data**:
    - If valid data is found, return it. Otherwise, return an empty dictionary.

### Codes

```python
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

```

## Bacdive

### Steps

1. **Retrieve Taxon ID**:  
   Get the `ncbi_taxon_id` from the `taxon` dictionary.

2. **Send GET Request to BacDive**:  
   Use `httpx.AsyncClient` to send a GET request to BacDive's search endpoint with the NCBI taxon ID.

3. **Parse HTML Response**:  
   Use BeautifulSoup to parse the response and extract links that contain strain URLs.

4. **Extract BacDive Taxon ID**:  
   Find the first strain URL from the parsed links and extract the BacDive taxon ID from the URL.

5. **Retry Mechanism**:  
   Implement a retry mechanism that attempts the request up to 5 times, with a 20-second delay between retries, if the request fails.

6. **Search in BacDive API**:  
   If the BacDive taxon ID is not found, use the BacDive client to search for data based on the species name.

7. **Return Retrieved Data**:  
   If the BacDive search is successful, return the retrieved data. Otherwise, return an empty dictionary.

### Codes

```python
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

```

## GBIF

### Steps

1. **Construct GBIF Match URL**:  
   Create the URL to fetch the species match data from GBIF using the species name from the portal dictionary.

2. **Send GET Request to GBIF**:  
   Use `httpx.AsyncClient` to send a GET request to the GBIF API to match the species name.

3. **Retry Mechanism**:  
   Implement a retry mechanism that attempts the request up to 5 times with a 20-second delay between retries if the request fails.

4. **Parse JSON Response**:  
   Convert the JSON response from the GBIF API into a Python dictionary.

5. **Extract Usage Key**:  
   Retrieve the `usageKey` from the parsed data. If the `usageKey` is not present, return an empty dictionary.

6. **Construct GBIF Occurrence URL**:  
   Create a new URL to fetch occurrence data from GBIF using the `usageKey`.

7. **Send GET Request for Occurrences**:  
   Use `httpx.AsyncClient` to send a GET request to the GBIF API to retrieve occurrence data based on the `usageKey`.

8. **Retry Mechanism for Occurrences**:  
   Implement the same retry mechanism for the occurrences request as done for the species match request.

9. **Return Retrieved Data**:  
   If the response contains results, return the first result. Otherwise, return an empty dictionary.

### Codes

```python
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

```

# API

For more details about this project's API, please visit the INNAKM API Docs.

Note: If the MkDocs server is running, please stop it and start the FastAPI server to access the documentation.

# Database

## Overview

This document provides an overview of the data structure and key fields in the database used for storing information about species from different portals. The database is organized into three main collections: `portals`, `raws`, and `terms`.

## Collections

### Taxa

The `taxa` collection stores data about taxon_id, ncbi_taxon_id, and species.

- **\_id**: MongoDB default identifier.
- **taxon_id**: A unique identifier for the taxon in the `taxa` collection.
- **ncbi_taxon_id**: NCBI-based ID for the taxon.
- **species**: The scientific name of the species.

**Example Document:**

```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxx",
  "taxon_id": 1,
  "ncbi_taxon_id": "Achromobacter mucicolens",
  "species": "wikidata"
}
```

### Portals

The `portals` collection stores data about portal_id, taxon_id, and web.

**Fields:**

- **\_id**: MongoDB default identifier.
- **portal_id**: A unique identifier for the taxon in the `portals` collection.
- **taxon_id**: A unique identifier for the taxon in the `taxa` collection as foreign key in `portals` collection.
- **web**: The source portal from which the data was retrieved (e.g., "wikidata").

**Example Document:**

```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxx",
  "portal_id": 1,
  "taxon_id": 1,
  "web": ["wikidata", "ncbi", "bacdive", "gbif"]
}
```

### Raws

The `raws` collection contains the raw fetched from the source portals.

**Fields:**

- **\_id**: MongoDB default identifier.
- **portal_id**: A unique identifier for the `portals` collection.
- **web**: The web source portal.
- **data**: The raw object.

**Example Document:**

```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxx",
  "portal_id": 1,
  "web": "wikidata",
  "data": {}
}
```

### Terms

The `terms` collection stores structured and detailed information about species.

#### Sections and Sources

| **Section**                                           | **Source** |
| ----------------------------------------------------- | ---------- |
| **Name and Taxonomic Classification**                 | NCBI       |
| **Morphology**                                        | BacDive    |
| **Culture and Growth Conditions**                     | BacDive    |
| **Physiology and Metabolism**                         | BacDive    |
| **Isolation, Sampling and Environmental Information** | BacDive    |
| **Safety Information**                                | BacDive    |
| **Sequence Information**                              | BacDive    |
| **Genome-based Prediction**                           | BacDive    |
| **Occurrences (georeference records)**                | GBIF       |

**Fields:**

- **\_id**: MongoDB default identifier.
- **taxon_id**: A unique identifier for the taxon in the `taxa` collection as foreign key in `portals` collection.
- **data**: The raw data that cleaned.

#### Example Document

```json
{
  "_id": "66e1dae562896968e8c5af10",
  "taxon_id": "1389922",
  "data": {
    "Name and taxonomic classification": {},
    "Morphology": {},
    "Culture and growth conditions": {},
    "Physiology and metabolism": {},
    "Isolation, sampling, and environmental information": {},
    "Safety information": {},
    "Sequence information": {},
    "Genome-based predictions": {},
    "Occurrence (georeference records)": {}
  }
}
```

## Setting Up the Search Index

To ensure that the search feature functionality works correctly, you must create a text index on the MongoDB collection. This index is essential for performing efficient text searches across multiple fields.

### Code for Creating the Search Index

Please send a request to `/terms/create-indexes` to create the indexes.

```python
# Check if indexes already exist
indexes = await term_collection.index_information()

# Create taxon_id index in taxon collection
await taxon_collection.create_index(
    "taxon_id",
    name="taxon_id_index_taxa",
    unique=True,
)

# Create ncbi_taxon_id index in taxon collection
await taxon_collection.create_index(
    "ncbi_taxon_id",
    name="ncbi_taxon_id_index_taxa",
    unique=True,
)

# Create taxon_id index in portal collection
await portal_collection.create_index(
    "taxon_id",
    name="taxon_id_index_portal",
    unique=True,
)

# Create portal_id index in portal collection
await portal_collection.create_index(
    "portal_id",
    name="portal_id_index_portal",
    unique=True,
)

# Create taxon_id index in term collection
await term_collection.create_index(
    "taxon_id",
    name="taxon_id_index",
    unique=True,
)

# Create text index in term collection
await term_collection.create_index(
    {"$**": "text"},
    name="search_index",
    language_override="none",
    default_language="en",
)
```

# Project Structure

## Backend Project Structure

**Backend Folder**

- **`__pycache__`**: Contains compiled Python files to speed up execution.

- **`app`**: Main application directory, including:

  - **`config.py`**: Configuration settings for the application.
  - **`database`**: MongoDB connection setup.
    - **`mongo.py`**: MongoDB setup and connection logic.
  - **`log`**: Log files for the application.
    - **`app.log`**: Application logs.
    - **`request.log`**: Request logs.
  - **`main.py`**: Entry point for the FastAPI application.
  - **`models`**: Data models for various entities.
    - **`base_model.py`**: Base model class for other models.
    - **`portal_model.py`**: Model for portal data.
    - **`raw_model.py`**: Model for raw data.
    - **`taxon_model.py`**: Model for taxon data.
    - **`term_model.py`**: Model for term data.
    - **`base_custom_model.py`**: Custom base model class.
  - **`operations`**: Scripts for data retrieval from different sources.
    - **`bacdive.py`**: Data retrieval logic from BacDive.
    - **`gbif.py`**: Data retrieval logic from GBIF.
    - **`ncbi.py`**: Data retrieval logic from NCBI.
    - **`wikidata.py`**: Data retrieval logic from WikiData.
  - **`routers`**: API route handlers.
    - **`portal_router.py`**: Routes for portal-related operations.
    - **`raw_router.py`**: Routes for raw data operations.
    - **`taxon_router.py`**: Routes for taxon-related operations.
    - **`term_router.py`**: Routes for term-related operations.
  - **`services`**: Service layer for business logic.
    - **`portal_service.py`**: Service logic for portals.
    - **`raw_service.py`**: Service logic for raw data.
    - **`taxon_service.py`**: Service logic for taxons.
    - **`term_service.py`**: Service logic for terms.
  - **`utils`**: Utility functions, decorators, message enumerations, and middleware components.
    - **`decorator`**: Custom decorators.
      - **`app_log_decorator.py`**: Decorator for logging application activities.
    - **`enum`**: Enumeration definitions for messages and status codes.
      - **`message_enum.py`**: Message enumeration.
      - **`status_code_enum.py`**: Status code enumeration.
    - **`helper`**: Helper functions for various operations.
      - **`func_helper.py`**: General helper functions.
      - **`map_terms_helper.py`**: Helper for mapping terms.
      - **`response_helper.py`**: Helper for handling responses.
    - **`middleware`**: Middleware components for request handling.
      - **`request_log_middleware.py`**: Middleware for logging requests.

- **`docs`**: Documentation files.

  - **`A.md`**: Documentation section A.
  - **`B.md`**: Documentation section B.
  - **`C.md`**: Documentation section C.
  - **`D.md`**: Documentation section D.
  - **`E.md`**: Documentation section E.
  - **`F.md`**: Documentation section F.
  - **`assets`**: Assets for documentation, including images.
    - **`logo_full.png`**: Full logo image.
    - **`logo_full_2.jpeg`**: Alternate full logo image.
    - **`logo_full_3.png`**: Another alternate full logo image.
    - **`logo_full_4.png`**: Additional alternate logo image.
  - **`index.md`**: Index for documentation.

- **`json`**: JSON files for various data.

  - **`ncbi_taxon_id.json`**: JSON file containing NCBI taxon IDs.
  - **`portal.json`**: JSON file for portal data.
  - **`portal_new.json`**: Updated JSON file for portal data.
  - **`species.json`**: JSON file for species data.
  - **`taxa.json`**: JSON file for taxa data.
  - **`terms.json`**: JSON file for terms data.
  - **`terms_data_example.json`**: Example JSON file for terms data.
  - **`terms_new.json`**: Updated JSON file for terms data.

- **`mkdocs.yml`**: Configuration file for MkDocs.

- **`requirements.txt`**: Project dependencies.

- **`venv`**: Virtual environment for the project.
