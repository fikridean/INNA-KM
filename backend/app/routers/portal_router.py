from typing import List
from fastapi import APIRouter, Query
from utils.helper.func_helper import handleError
from models.portal_model import PortalCreateModel, PortalCreateResponseModel, PortalCreateResponseModelObject, PortalDeleteModel, PortalDeleteResponseModel, PortalDeleteResponseModelObject, PortalDetailModel, PortalDetailResponseModel, PortalDetailResponseModelObject, PortalGetModel, PortalGetResponseModel, PortalGetResponseModelObject, PortalRetrieveDataModel, PortalRetrieveDataResponseModel, PortalRetrieveDataResponseModelObject
from services.portal_service import get_portals, get_portal_detail, retrieve_data, create_portal, delete_portal
from utils.helper.response_helper import success_response, error_response
from utils.enum.message_enum import ResponseMessage
from utils.enum.status_code_enum import StatusCode

router = APIRouter()

# Create or Update portal
@router.post('/create', response_model=PortalCreateResponseModel, status_code=StatusCode.CREATED.value)
async def create_portal_route_func(params: List[PortalCreateModel]):
    try:
        data: List[PortalCreateResponseModelObject] = await create_portal(params)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=StatusCode.CREATED.value)
    
    except Exception as e:
        return handleError(e)

# Get portals
@router.post("/get", response_model=PortalGetResponseModel, status_code=StatusCode.OK.value)
async def get_portals_route_func(params: PortalGetModel):
    try:
        data: List[PortalGetResponseModelObject] = await get_portals(params)
        return success_response(data, message=ResponseMessage.OK_LIST.value, status_code=StatusCode.OK.value)
    
    except Exception as e:
        return handleError(e)

# Get portal detail
@router.get("/detail", response_model=PortalDetailResponseModel, status_code=StatusCode.OK.value)
async def get_portal_detail_route_func(params: PortalDetailModel = Query(...)):
    try:
        data: PortalDetailResponseModelObject = await get_portal_detail(params)
        return success_response(data, message=ResponseMessage.OK.value, status_code=StatusCode.OK.value)
    
    except Exception as e:
        return handleError(e)

# Delete portal
@router.delete('/delete', response_model=PortalDeleteResponseModel, status_code=StatusCode.OK.value)
async def delete_portal_route_func(params: PortalDeleteModel):
    try:
        data: List[PortalDeleteResponseModelObject] = await delete_portal(params)
        return success_response(data, message=ResponseMessage.OK_DELETE.value, status_code=StatusCode.OK.value)
    
    except Exception as e:
        return handleError(e)

# Retrieve data
@router.get('/retrieve-data', response_model=PortalRetrieveDataResponseModel, status_code=StatusCode.OK.value)
async def retrieve_data_route_func(params: PortalRetrieveDataModel = Query(...)):
    try:        
        data: PortalRetrieveDataResponseModelObject = await retrieve_data(params)
        return success_response(data, message=ResponseMessage.OK.value, status_code=StatusCode.OK.value)
    
    except Exception as e:
        return handleError(e)