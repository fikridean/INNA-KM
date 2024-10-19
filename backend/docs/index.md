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