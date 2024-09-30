from typing import List
from fastapi import APIRouter, Query, status
from models.portal_model import PortalBaseModel, PortalCreateResponseModel, PortalDeleteModel, PortalDeleteResponseModel, PortalDetailModel, PortalDetailResponseModel, PortalGetWithDetailWebResponseModel, PortalGetModel, PortalGetResponseModel, PortalRetrieveDataModel, PortalRetrieveDataResponseModel
from services.portal_service import get_portals, get_portal_detail, get_portals_with_web_detail, retrieve_data, create_portal, delete_portal
from utils.helper.response_helper import success_response, error_response
from utils.message.message_enum import ResponseMessage

router = APIRouter()

# Retrieve data
@router.get('/retrieve-data', response_model=PortalRetrieveDataResponseModel, status_code=status.HTTP_200_OK)
async def retrieve_data_route_func(params: PortalRetrieveDataModel = Query(...)):
    try:
        data = await retrieve_data(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Create or Update portal
@router.post('/create', response_model=PortalCreateResponseModel, status_code=status.HTTP_201_CREATED)
async def create_portal_route_func(params: List[PortalBaseModel]):
    try:
        data = await create_portal(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=201)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Delete portal
@router.delete('/delete', response_model=PortalDeleteResponseModel, status_code=status.HTTP_200_OK)
async def delete_portal_route_func(params: PortalDeleteModel):
    try:
        data = await delete_portal(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK_DELETE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Get portals with detail
@router.post("/get/web-detail", response_model=PortalGetWithDetailWebResponseModel, status_code=status.HTTP_200_OK)
async def get_portals_with_web_detail_route_func(params: PortalGetModel):
    try:
        data = await get_portals_with_web_detail(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)

        return success_response(data, message=ResponseMessage.OK_LIST.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Get portals
@router.post("/get", response_model=PortalGetResponseModel, status_code=status.HTTP_200_OK)
async def get_portals_route_func(params: PortalGetModel):
    try:
        data = await get_portals(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK_LIST.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Get portal detail
@router.get("/detail", response_model=PortalDetailResponseModel, status_code=status.HTTP_200_OK)
async def get_portal_detail_route_func(params: PortalDetailModel = Query(...)):
    try:
        data = await get_portal_detail(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)