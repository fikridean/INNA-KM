from typing import List
from fastapi import APIRouter
from utils.helper.func_helper import handleError
from utils.enum.status_code_enum import StatusCode
from services.raw_service import store_raw_from_portals, delete_raw_from_db, get_raw
from utils.helper.response_helper import success_response
from utils.enum.message_enum import ResponseMessage
from models.raw_model import (
    RawDeleteResponseModel,
    RawDeleteResponseModelObject,
    RawGetModel,
    RawGetResponseModel,
    RawGetResponseModelObject,
    RawStoreModel,
    RawDeleteModel,
    RawStoreResponseModel,
    RawStoreResponseModelObject,
)

router = APIRouter()


# Store raw
@router.post(
    "/store", response_model=RawStoreResponseModel, status_code=StatusCode.CREATED.value
)
async def store_raw_from_portal_route_func(params: RawStoreModel):
    try:
        data: List[RawStoreResponseModelObject] = await store_raw_from_portals(params)
        return success_response(
            data,
            message=ResponseMessage.OK_CREATEORUPDATE.value,
            status_code=StatusCode.CREATED.value,
        )

    except Exception as e:
        return handleError(e)


# Get raw
@router.post(
    "/get", response_model=RawGetResponseModel, status_code=StatusCode.OK.value
)
async def get_raw_route_func(params: RawGetModel):
    try:
        data: List[RawGetResponseModelObject] = await get_raw(params)
        return success_response(
            data, message=ResponseMessage.OK.value, status_code=StatusCode.OK.value
        )

    except Exception as e:
        return handleError(e)


# Delete raw
@router.delete(
    "/delete", response_model=RawDeleteResponseModel, status_code=StatusCode.OK.value
)
async def delete_raw_route_func(params: RawDeleteModel):
    try:
        data: List[RawDeleteResponseModelObject] = await delete_raw_from_db(params)
        return success_response(
            data,
            message=ResponseMessage.OK_DELETE.value,
            status_code=StatusCode.OK.value,
        )

    except Exception as e:
        return handleError(e)
