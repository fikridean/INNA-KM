from fastapi import APIRouter
from utils.enum.status_code_enum import StatusCode
from utils.helper.func_helper import handleError
from services.term_service import (
    create_indexes,
    delete_term,
    get_terms,
    search_terms,
    store_raw_to_terms,
)
from utils.helper.response_helper import success_response
from utils.enum.message_enum import ResponseMessage
from models.term_model import (
    TermDeleteModel,
    TermDeleteResponseModel,
    TermGetModel,
    TermGetResponseModel,
    TermStoreResponseModel,
    searchModel,
    TermStoreModel,
    searchResponseModel,
)

router = APIRouter()


# Create or update term
@router.post(
    "/create",
    response_model=TermStoreResponseModel,
    status_code=StatusCode.CREATED.value,
)
async def create_term_route_func(params: TermStoreModel):
    try:
        data = await store_raw_to_terms(params)
        return success_response(
            data,
            message=ResponseMessage.OK_CREATEORUPDATE.value,
            status_code=StatusCode.OK.value,
        )

    except Exception as e:
        return handleError(e)


# Get all terms
@router.post(
    "/get", response_model=TermGetResponseModel, status_code=StatusCode.OK.value
)
async def get_term_route_func(params: TermGetModel):
    try:
        data = await get_terms(params)
        return success_response(
            data, message=ResponseMessage.OK.value, status_code=StatusCode.OK.value
        )

    except Exception as e:
        return handleError(e)


# Delete term
@router.delete(
    "/delete", response_model=TermDeleteResponseModel, status_code=StatusCode.OK.value
)
async def delete_term_route_func(params: TermDeleteModel):
    try:
        data = await delete_term(params)
        return success_response(
            data,
            message=ResponseMessage.OK_DELETE.value,
            status_code=StatusCode.OK.value,
        )

    except Exception as e:
        return handleError(e)


# Search terms
@router.post(
    "/search", response_model=searchResponseModel, status_code=StatusCode.OK.value
)
async def search_term_route_func(params: searchModel):
    try:
        data = await search_terms(params)
        return success_response(
            data, message=ResponseMessage.OK.value, status_code=StatusCode.OK.value
        )

    except Exception as e:
        return handleError(e)


# Create indexes
@router.get("/create-indexes", status_code=StatusCode.CREATED.value)
async def create_indexes_route_func():
    try:
        data = await create_indexes()
        return success_response(
            data,
            message=ResponseMessage.OK_CREATE.value,
            status_code=StatusCode.CREATED.value,
        )

    except Exception as e:
        return handleError(e)
