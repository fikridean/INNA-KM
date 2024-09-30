# Database

## Overview

This document provides an overview of the data structure and key fields in the database used for storing information about species from different portals. The database is organized into three main collections: `portals`, `raws`, and `terms`.

## Collections

### Portals

The `portals` collection stores metadata about the species and the source portal.

**Fields:**

- **\_id**: Unique identifier for the portal entry.
- **taxon_id**: A unique identifier for the species in the source portal.
- **species**: The scientific name of the species.
- **web**: The source portal from which the data was retrieved (e.g., "wikidata").

**Example Document:**

```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxx",
  "taxon_id": "1389922",
  "species": "Achromobacter mucicolens",
  "web": "wikidata"
}
```

### Raws

The `raws` collection contains the raw fetched from the source portals.

**Fields:**

- **\_id**: Unique identifier for the raw entry.
- **taxon_id**: A unique identifier for the species.
- **species**: The scientific name of the species.
- **web**: The source portal.
- **data**: The raw object.

**Example Document:**

```json
{
  "_id": "66e1a32f62896968e859ff66",
  "taxon_id": "1389922",
  "species": "Achromobacter mucicolens",
  "data": {}
}
```

### Terms

The `terms` collection stores structured and detailed information about species.

#### Sections and Sources

| **Section**                                           | **Source**            |
| ----------------------------------------------------- | --------------------- |
| **Name and Taxonomic Classification**                 | NCBI                  |
| **Morphology**                                        | BacDive               |
| **Culture and Growth Conditions**                     | BacDive               |
| **Physiology and Metabolism**                         | BacDive               |
| **Isolation, Sampling and Environmental Information** | BacDive               |
| **Safety Information**                                | BacDive               |
| **Sequence Information**                              | BacDive               |
| **Genome-based Prediction**                           | BacDive               |
| **Occurrences (georeference records)**                | GBIF                  |

**Fields:**

- **\_id**: Unique identifier for the term entry.
- **taxon_id**: A unique identifier for the species.
- **species**: The scientific name of the species.
- **data**: Contains various categories of information about the species

#### Example Document

```json
{
  "_id": "66e1dae562896968e8c5af10",
  "taxon_id": "1389922",
  "species": "Achromobacter mucicolens",
  "data": {
    "Name and taxonomic classification": {},
    "Morphology": {},
    "Culture and growth conditions": {},
    "Physiology and metabolism": {},
    "Isolation, sampling, and environmental information": {},
    "Safety information": {},
    "Sequence information": {},
    "Genome-based predictions": {},
    "Occurrence (georeference records)": {},
  },
}
```


## Setting Up the Search Index

To ensure that the search feature functionality works correctly, you must create a text index on the MongoDB collection. This index is essential for performing efficient text searches across multiple fields.

### Code for Creating the Search Index

Please send a request to `/terms/create-indexes` to create the indexes.

```python
indexes = await terms_collection.index_information()

await terms_collection.create_index(
    { "$**": "text" },
    name='search_index',
    weights={
        "taxon_id": 10,
        "species": 8,
        "data": 6
    },
    language_override='none',
    default_language='en',
)

await terms_collection.create_index(
    "taxon_id",
    name='taxon_id_index',
    unique=True,
)

await terms_collection.create_index(
    "species",
    name='species_index',
)
```
