from fastapi import APIRouter, status
from services.raw_service import get_raw_with_web_detail, store_raw_from_portals, delete_raw_from_db, get_raw
from utils.helper.response_helper import success_response, error_response
from utils.message.message_enum import ResponseMessage
from models.raw_model import RawDeleteResponseModel, RawGetModel, RawGetResponseModel, RawGetWithWebDetailResponseModel, RawStoreModel, RawDeleteModel, RawStoreResponseModel
router = APIRouter()

# Get raw
@router.post('/get', response_model=RawGetResponseModel, status_code=status.HTTP_200_OK)
async def get_raw_route_func(params: RawGetModel):
    try:
        data = await get_raw(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Get raw with web detail
@router.post('/get/web-detail', response_model=RawGetWithWebDetailResponseModel, status_code=status.HTTP_200_OK)
async def get_raw__with_web_detail_route_func(params: RawGetModel):
    try:
        data = await get_raw_with_web_detail(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Store raw
@router.post('/store', response_model=RawStoreResponseModel, status_code=status.HTTP_200_OK)
async def store_raw_from_portal_route_func(params: RawStoreModel):
    try:
        data = await store_raw_from_portals(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Delete raw
@router.delete('/delete', response_model=RawDeleteResponseModel, status_code=status.HTTP_200_OK)
async def delete_raw_route_func(params: RawDeleteModel):
    try:
        data = await delete_raw_from_db(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK_DELETE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
