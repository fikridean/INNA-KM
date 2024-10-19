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

- **\_id**: MongoDB default identifier.
- **taxon_id**: A unique identifier for the taxon in the `taxa` collection as foreign key in `portals` collection.
- **data**: The raw data that cleaned.

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
