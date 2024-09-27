# Database

## Overview

This document provides an overview of the data structure and key fields in the database used for storing information about species from different portals. The database is organized into three main collections: `portals`, `raws`, and `terms`.

## Collections

### Portals

The `portals` collection stores metadata about the species and the source portal.

**Fields:**

- **\_id**: Unique identifier for the portal entry.
- **species**: The scientific name of the species.
- **web**: The source portal from which the data was retrieved (e.g., "wikidata").
- **slug**: A URL-friendly identifier derived from the species name and portal.
- **taxon_id**: A unique identifier for the species in the source portal.

**Example Document:**

```json
{
  "_id": "66e1d78c62896968e8bf390a",
  "species": "Achromobacter mucicolens",
  "web": "wikidata",
  "slug": "wikidata-achromobacter-mucicolens",
  "taxon_id": "1389922"
}
```

### Raws

The `raws` collection contains the raw data fetched from the source portals.

**Fields:**

- **\_id**: Unique identifier for the raw data entry.
- **slug**: A URL-friendly identifier for the species.
- **data**: The raw data object, which includes:
  - **entities**: Contains the main data entities.
    - **success**: Indicates the success of the data retrieval.
    - **species**: The scientific name of the species.
    - **web**: The source portal.

**Example Document:**

```json
{
  "_id": "66e1a32f62896968e859ff66",
  "slug": "wikidata-achromobacter-mucicolens",
  "data": {
    "entities": {
      "success": "1",
      "species": "Achromobacter mucicolens",
      "web": "wikidata"
    }
  }
}
```

### Terms

The `terms` collection stores structured and detailed information about species.

**Fields:**

- **\_id**: Unique identifier for the term entry.
- **species**: The scientific name of the species.
- **data**: Contains various categories of information about the species:
  - **Name and taxonomic classification**: Classification details of the species.
  - **Occurrence (georeference records)**: Records related to the geographical occurrences of the species.
  - **Morphology**: Information on the physical characteristics and morphology of the species.
  - **Culture and growth conditions**: Details about how the species is cultured and its growth conditions.
  - **Physiology and metabolism**: Information on the physiological processes and metabolism of the species.
  - **Isolation, sampling, and environmental information**: Data on how the species is isolated, sampled, and the environmental conditions.
  - **Safety information**: Safety-related information regarding the species.
  - **Sequence information**: Genetic sequence data related to the species.
  - **web**: The source portal from which the data was obtained.

### Example Document

```json
{
  "_id": "66e1dae562896968e8c5af10",
  "species": "Achromobacter mucicolens",
  "data": {
    "Name and taxonomic classification": {},
    "Occurrence (georeference records)": {},
    "Morphology": {},
    "Culture and growth conditions": {},
    "Physiology and metabolism": {},
    "Isolation, sampling, and environmental information": {},
    "Safety information": {},
    "Sequence information": {}
  },
  "web": "wikidata"
}
```

## Setting Up the Search Index

To ensure that the search feature functionality works correctly, you must create a text index on the MongoDB collection. This index is essential for performing efficient text searches across multiple fields.

### Code for Creating the Search Index

In the `term_crud` file, you will find the following code commented within the `search_terms` function. This code creates a text index for the search feature:

```python
indexes = await raw_collection.index_information()
print(indexes)

await raw_collection.create_index(
    { "$**": "text" },
    name='search_index',
    weights={
        "web": 10,
        "species": 10,
        "slug": 8,
        "data": 7
    },
    language_override='none',
    default_language='en',
)
```
