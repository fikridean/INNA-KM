from fastapi import APIRouter, status
from services.raw_service import store_raw_from_portals, delete_raw_from_db, get_raw
from utils.helper.response_helper import success_response, error_response
from utils.message.message_enum import ResponseMessage
from models.raw_model import RawDeleteResponseModel, RawGetModel, RawGetResponseModel, RawStoreModel, RawDeleteModel, RawStoreResponseModel
router = APIRouter()

@router.get('/get', response_model=RawGetResponseModel, status_code=status.HTTP_200_OK)
async def get_raw_route_func(params: RawGetModel):
    try:
        data = await get_raw(params)
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

@router.post('/store', response_model=RawStoreResponseModel, status_code=status.HTTP_200_OK)
async def store_raw_from_portal_route_func(params: RawStoreModel):
    try:
        data = await store_raw_from_portals(params)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
    
@router.delete('/delete', response_model=RawDeleteResponseModel, status_code=status.HTTP_200_OK)
async def delete_raw_route_func(params: RawDeleteModel):
    try:
        data = await delete_raw_from_db(params)
        return success_response(data, message=ResponseMessage.OK_DELETE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
