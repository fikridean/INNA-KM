# Introduction
This project is a FastAPI-based web service that interacts with a MongoDB database using Motor, an async MongoDB driver for Python. The service retrieves, processes, and stores data across three main collections: portals, raw data, and terms.

This project is designed to facilitate the management of information across different stages of data processing. It includes functionality for:

- Managing portal-related data.
- Collecting and storing raw data.
- Processing raw data into terms, which are then stored for later use.