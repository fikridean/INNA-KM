# Data Parsing
## Why is data parsing needed before adding data to the database?
Before inserting data into the database, it is crucial to follow the appropriate data parsing steps for each portal. Data parsing ensures that the data is correctly retrieved, processed, and transformed into the desired format before being stored.

## Wikidata - Fetching Data from Wikidata using NCBI Taxon ID

### Steps

1. **Define Variables**:  
    Set the `NCBI_TAXON_ID_CODE` and retrieve the `taxon_id` from the portal.

2. **Formulate SPARQL Query**:  
    Construct a SPARQL query to fetch the entity using the `taxon_id`.

3. **Send SPARQL Query Request**:  
    Use `httpx.AsyncClient` to send a GET request to the Wikidata SPARQL endpoint.

4. **Retry Mechanism**:  
    Implement a retry mechanism that attempts the request up to 5 times if it fails, with a 20-second delay between retries.

5. **Check for Empty Data**:  
    After receiving the response, check if the data is empty or if there are no results.

6. **Extract the ID**:  
    Extract the entity ID from the SPARQL query response.

7. **Fetch Entity Data**:  
    Construct a new URL to fetch the entity's data using the extracted ID and make another GET request to Wikidata’s API.

8. **Retry Mechanism for Entity Data**:  
    Apply the same retry mechanism for this request as well.

9. **Return Data**:  
    If the entity data is found, return it. Otherwise, return an empty dictionary.

### Codes

```python
async def retrieve(portal: dict) -> dict:
    # Define the NCBI taxon ID property from Wikidata
    NCBI_TAXON_ID_CODE = 'P685'

    # Get the taxon ID from the portal
    portal_taxon_id = portal['taxon_id']

    # Construct the SPARQL query to fetch the item using the taxon ID
    query = f"""
        SELECT ?item WHERE {{
        ?item wdt:{NCBI_TAXON_ID_CODE} "{portal_taxon_id}".
        }}
    """

    # Define the request headers for the SPARQL query
    headers = {
        "Accept": "application/sparql-results+json"
    }

    # Initialize an empty dictionary for the data
    data = {}

    # Send the SPARQL query using an asynchronous HTTP client
    async with httpx.AsyncClient() as client:
        retry_count = 0
        while retry_count < 5:  # Retry the request up to 5 times
            try:
                # Send GET request to Wikidata SPARQL endpoint
                response = await client.get(WIKIDATA_SPARQL_URL, params={"query": query}, headers=headers)
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
    if not data['results']['bindings']:
        return {}

    # Extract the entity ID from the query results
    id = data['results']['bindings'][0]['item']['value'].split('/')[-1]

    # Return an empty dictionary if the ID is empty
    if not id:
        return {}

    # Construct the URL to fetch detailed data for the entity using its ID
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={id}&languages=en"

    # Send a GET request to the Wikidata API to retrieve the entity data
    async with httpx.AsyncClient() as client:
        retry_count = 0
        while retry_count < 5:  # Retry up to 5 times if the request fails
            try:
                # Send GET request to Wikidata API to fetch the entity details
                response = await client.get(url)
                response.raise_for_status()  # Raise exception if the response status is an error
                
                # Parse the response as JSON
                data = response.json()
                break  # Exit the loop if the request was successful

            except httpx.HTTPError:
                # If the request fails, print a retry message and wait for 20 seconds before retrying
                print(f"Retrying after 20 seconds for {portal['species']}")
                await asyncio.sleep(20)
                retry_count += 1
                continue  # Retry the request

    # If no data was returned, return an empty dictionary
    if not data:
        return {}

    # If the entity is not found in the response, return an empty dictionary
    if not data['entities'][id]:
        return {}

    # Return the data fetched from Wikidata
    return data

```

## NCBI - Fetching Data from NCBI using Taxon ID

### Steps

1. **Define Variables**:  
    Retrieve the `taxon_id` from the provided portal dictionary.

2. **Construct URL**:  
    Build the URL to fetch data from NCBI using the extracted taxon ID.

3. **Send GET Request**:  
    Use `httpx.AsyncClient` to send a GET request to the NCBI API.

4. **Retry Mechanism**:  
    Implement a retry mechanism that attempts the request up to 5 times if it fails, with a 20-second delay between retries.

5. **Parse XML Response**:  
    Convert the XML response from the NCBI API into a Python dictionary using `xmltodict`.

6. **Check for Empty Data**:  
    Ensure the response contains valid data before proceeding.

7. **Return Data**:  
    If valid data is found, return it. Otherwise, return an empty dictionary.

### Codes

```python
async def retrieve(portal: dict) -> dict:
    # Get the taxon ID from the portal
    portal_taxon_id = portal['taxon_id']

    # Construct a new URL to fetch data by the extracted ID
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id={portal_taxon_id}"

    data = {}

    # Create another asynchronous HTTP client session
    async with httpx.AsyncClient() as client:
        retry_count = 0
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
    if not data['TaxaSet']['Taxon']:
        return {}

    # Extract the 'Taxon' data
    data = data['TaxaSet']['Taxon']

    # Return the parsed data
    return data
```

## Bacdive - Fetching Data from BacDive using NCBI Taxon ID

### Steps

1. **Retrieve Taxon ID**:  
    Get the `taxon_id` from the `portal` dictionary.

2. **Send GET Request to BacDive**:  
    Use `httpx.AsyncClient` to send a GET request to BacDive's search endpoint with the NCBI taxon ID.

3. **Parse HTML Response**:  
    Use BeautifulSoup to parse the response and extract links that contain strain URLs.

4. **Extract BacDive Taxon ID**:  
    Find the first strain URL from the parsed links and extract the BacDive taxon ID from the URL.

5. **Retry Mechanism**:  
    Implement a retry mechanism that attempts the request up to 5 times, with a 20-second delay between retries, if the request fails.

6. **Search in BacDive API**:  
    Use the BacDive client to search for data based on the extracted BacDive taxon ID.

7. **Return Retrieved Data**:  
    If the BacDive search is successful, return the retrieved data. Otherwise, return an empty dictionary.

### Codes

```python
async def retrieve(portal: dict) -> dict:
    # Get the taxon ID from the portal
    taxon_id = portal['taxon_id']

    bacdive_taxon_id = {}

    # Send a request to BacDive search page using the taxon ID
    async with httpx.AsyncClient() as client:
        retry_count = 0
        while retry_count < 5:  # Retry the request up to 5 times if it fails
            try:
                # Send a GET request to BacDive search URL with NCBI taxon ID
                response = await client.get(f'https://bacdive.dsmz.de/advsearch?fg%5B0%5D%5Bgc%5D=OR&fg%5B0%5D%5Bfl%5D%5B1%5D%5Bfd%5D=16S+associated+NCBI+tax+ID&fg%5B0%5D%5Bfl%5D%5B1%5D%5Bfo%5D=equal&fg%5B0%5D%5Bfl%5D%5B1%5D%5Bfv%5D={taxon_id}&fg%5B0%5D%5Bfl%5D%5B1%5D%5Bfvd%5D=sequence_16S-tax_id-7')
                # Raise an exception if the request was unsuccessful
                response.raise_for_status()

                # Parse the HTML response using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all 'a' tags and extract the URLs from the href attributes
                links = soup.find_all('a')
                hrefs = [link.get('href') for link in links]

                # Extract the first strain URL and retrieve BacDive taxon ID
                first_strain_url = next((url for url in hrefs if url.startswith('/strain/')), None)

                if not first_strain_url:
                    return {}

                bacdive_taxon_id = first_strain_url.split('/')[-1]

                break  # Break out of the loop if successful

            except httpx.HTTPError:
                # Retry after waiting for 20 seconds if an error occurs
                print(f"Retrying after 20 seconds for {portal['species']}")
                await asyncio.sleep(20)
                retry_count += 1
                continue  # Retry if unsuccessful

    # Return an empty dict if BacDive taxon ID is not found
    if not bacdive_taxon_id:
        return {}

    # Use BacDive client to search for data by BacDive taxon ID
    bacdive_client = bacdive.BacdiveClient(BACDIVE_EMAIL, BACDIVE_PASSWORD)
    query = {"id": bacdive_taxon_id}
    bacdive_client.search(**query)

    # Return the retrieved data or an empty dict if no data is found
    if not bacdive_client.retrieve():
        return {}

    # Return the first result of the retrieved data
    return next(bacdive_client.retrieve())
```

## GBIF - Fetching Data from GBIF using Species Name

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
async def retrieve(portal: dict) -> dict:
    # Construct the URL for GBIF species match API using the species name
    url = f'https://api.gbif.org/v1/species/match?name={portal["species"]}'

    data = {}

    async with httpx.AsyncClient() as client:
        retry_count = 0
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
    usage_key = data.get('usageKey')
    if not usage_key:
        return {}
    
    # Construct the URL for GBIF occurrence API using the usageKey
    url = f'https://api.gbif.org/v1/occurrence/search?taxonKey={usage_key}'

    async with httpx.AsyncClient() as client:
        retry_count = 0
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
    if not data['results'][0]:
        return {}

    return data['results'][0]

