from typing import List
from fastapi import APIRouter, status
from services.term_service import delete_term, get_terms, search_terms, store_raw_to_terms
from utils.helper.response_helper import success_response, error_response
from utils.message.message_enum import ResponseMessage
from models.term_model import TermDeleteModel, TermGetModel, searchParams, TermStoreModel, TermStoreFromRawModel, termBaseModel
router = APIRouter()

# Create or update term
@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_term_route_func(params: List[TermStoreModel]):
    try:
        data = await store_raw_to_terms(params)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Get all terms
@router.get('/', status_code=status.HTTP_200_OK)
async def get_term_route_func(params: TermGetModel):
    try:
        data = await get_terms(params)
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
    
# Delete term
@router.delete('/', status_code=status.HTTP_200_OK)
async def delete_term_route_func(params: TermDeleteModel):
    try:
        data = await delete_term(params)
        return success_response(data, message=ResponseMessage.OK_DELETE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Search terms
@router.post('/search', status_code=status.HTTP_200_OK)
async def search_term_route_func(params: searchParams):
    try:
        data = await search_terms(params)
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)