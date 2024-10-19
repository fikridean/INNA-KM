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
