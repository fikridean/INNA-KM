from fastapi import APIRouter, status
from services.term_service import create_indexes, delete_term, get_terms, search_terms, store_raw_to_terms
from utils.helper.response_helper import success_response, error_response
from utils.message.message_enum import ResponseMessage
from models.term_model import TermDeleteModel, TermDeleteResponseModel, TermGetModel, TermGetResponseModel, TermStoreResponseModel, searchModel, TermStoreModel, searchResponseModel
router = APIRouter()

# Create or update term
@router.post('/create', response_model=TermStoreResponseModel, status_code=status.HTTP_201_CREATED)
async def create_term_route_func(params: TermStoreModel):
    try:
        data = await store_raw_to_terms(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Get all terms
@router.post('/get', response_model=TermGetResponseModel, status_code=status.HTTP_200_OK)
async def get_term_route_func(params: TermGetModel):
    try:
        data = await get_terms(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Delete term
@router.delete('/delete', response_model=TermDeleteResponseModel, status_code=status.HTTP_200_OK)
async def delete_term_route_func(params: TermDeleteModel):
    try:
        data = await delete_term(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        if all(item['status'] == 'not_found' for item in data):
            return error_response(data, message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK_DELETE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Search terms
@router.post('/search', response_model=searchResponseModel, status_code=status.HTTP_200_OK)
async def search_term_route_func(params: searchModel):
    try:
        data = await search_terms(params)

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
    
# Create indexes
@router.get('/create-indexes', status_code=status.HTTP_200_OK)
async def create_indexes_route_func():
    try:
        data = await create_indexes()

        if data is None or len(data) == 0:
            return error_response(message=ResponseMessage.NO_DATA.value, status_code=404)
        
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)