from enum import Enum


# For outer response
class ResponseMessage(Enum):
    # Data Related
    OK = "Successfully get data"
    OK_LIST = "Successfully get list of data"
    OK_CREATE = "Successfully create data"
    OK_UPDATE = "Successfully update data"
    OK_CREATEORUPDATE = "Successfully create or update data"
    OK_DELETE = "Successfully delete data"

    # Error Related
    ERR = "Failed to get data"
    ERR_LIST = "Failed to get list of data"
    ERR_CREATE = "Failed to create data"
    ERR_UPDATE = "Failed to update data"
    ERR_DELETE = "Failed to delete data"
    ERR_RESULTS_NOT_FOUND = "No results found"

    # Server Error
    ERR_INTERNAL_SERVER_ERROR = "Internal server error"
    ERR_NOT_IMPLEMENTED = "Not implemented"
    ERR_BAD_GATEWAY = "Bad gateway"

    # Client Error
    ERR_BAD_REQUEST = "Bad request"
    ERR_UNAUTHORIZED = "Unauthorized"
    ERR_FORBIDDEN = "Forbidden"
    ERR_NOT_FOUND = "Not found"
    ERR_METHOD_NOT_ALLOWED = "Method not allowed"
    ERR_REQUEST_TIMEOUT = "Request timeout"
    ERR_TOO_MANY_REQUESTS = "Too many requests"

    INVALID_QUERY_PARAMS = "Invalid query parameters"
    INVALID_PAYLOAD = "No data was provided in the request payload. Please include the required fields and try again."
    INVALID_PAYLOAD_SECURITY = "A valid identifier is required for this operation. Please provide the necessary data and try again."


# For inner data retrieval
class InfoMessage(Enum):
    DATA_RETRIEVED = "Data retrieved successfully"
    DATA_RETRIEVED_AND_STORED = "Data retrieved and stored successfully"
    DATA_PARTIALLY_RETRIEVED_AND_STORED = (
        "Data partially retrieved and stored successfully"
    )
    DATA_RETRIEVED_AND_STORED_FROM_ALL_WEB = (
        "Data retrieved and stored from all web successfully"
    )
    DATA_RETRIEVED_AND_STORED_FROM_SOME_WEB = (
        "Data retrieved and stored from some web successfully"
    )
    DATA_CREATED = "Data created successfully"
    DATA_UPDATED = "Data updated successfully"
    DATA_DELETED = "Data deleted successfully"

    DATA_NOT_RETRIEVED = "Data retrieval failed"
    DATA_NOT_RETRIEVED_AND_STORED = "Data retrieval and storage failed"
    DATA_NOT_RETRIEVED_AND_STORED_FROM_ALL_WEB = (
        "Data retrieval and storage from all web failed"
    )
    DATA_NOT_RETRIEVED_AND_STORED_FROM_SOME_WEB = (
        "Data retrieval and storage from some web failed"
    )
    DATA_NOT_CREATED = "Data creation failed"
    DATA_NOT_UPDATED = "Data update failed"
    DATA_NOT_DELETED = "Data deletion failed"

    # Exist
    TAXON_EXIST = "Taxon already exist"
    PORTAL_EXIST = "Portal already exist"
    RAW_EXIST = "Raw data already exist"
    TERMS_EXIST = "Terms already exist"
    TAXON_WITH_SPECIES_AND_NCBI_TAXON_ID_EXIST = (
        "Taxon with species and ncbi_taxon_id already exist"
    )
    PORTAL_WITH_TAXON_ID_EXIST = "Portal with taxon_id already exist"

    TAXON_NOT_EXIST = "Taxon does not exist"
    PORTAL_NOT_EXIST = "Portal does not exist"
    RAW_NOT_EXIST = "Raw data does not exist"
    TERMS_NOT_EXIST = "Terms does not exist"

    # Used
    TAXON_USED = "Taxon is used in other collections"
    PORTAL_USED = "Portal is used in other collections"


class StatusMessage(Enum):
    DATA_FOUND = "Found"
    DATA_PARTIALLY_FOUND = "Partially found"
    DATA_SUCCESS = "Success"

    DATA_NOT_FOUND = "Not found"
    DATA_FAILED = "Failed"


class SpeciesMessage(Enum):
    SPECIES_NOT_FOUND = "Species not found"
    SPECIES_FOUND = "Species found"
