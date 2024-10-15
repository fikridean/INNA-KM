from typing import List
from fastapi import APIRouter, Query
from utils.helper.func_helper import handleError
from models.taxon_model import (
    TaxonBaseModel,
    TaxonBaseResponseModel,
    TaxonBaseResponseModelObject,
    TaxonDeleteModel,
    TaxonGetDetailModel,
    TaxonGetDetailResponseModel,
    TaxonGetModel,
    TaxonGetResponseModel,
    TaxonGetResponseModelObject,
)
from services.taxon_service import (
    create_taxon,
    delete_taxon,
    get_taxon,
    get_taxon_details,
)
from utils.helper.response_helper import success_response, error_response
from utils.enum.message_enum import ResponseMessage
from utils.enum.status_code_enum import StatusCode

router = APIRouter()


# Create or Update taxon
@router.post(
    "/create",
    response_model=List[TaxonBaseResponseModel],
    status_code=StatusCode.CREATED.value,
)
async def create_taxon_route_func(params: List[TaxonBaseModel]):
    try:
        data: List[TaxonBaseResponseModelObject] = await create_taxon(params)
        return success_response(
            data,
            message=ResponseMessage.OK_CREATEORUPDATE.value,
            status_code=StatusCode.CREATED.value,
        )

    except Exception as e:
        return handleError(e)


# Get all taxa
@router.post(
    "/get", response_model=List[TaxonGetResponseModel], status_code=StatusCode.OK.value
)
async def get_taxon_route_func(params: TaxonGetModel):
    try:
        data: List[TaxonGetResponseModelObject] = await get_taxon(params)
        return success_response(
            data, message=ResponseMessage.OK.value, status_code=StatusCode.OK.value
        )

    except Exception as e:
        return handleError(e)


# Get taxon details
@router.get(
    "/detail",
    response_model=TaxonGetDetailResponseModel,
    status_code=StatusCode.OK.value,
)
async def get_taxon_details_route_func(params: TaxonGetDetailModel = Query(...)):
    try:
        data: TaxonGetResponseModelObject = await get_taxon_details(params)
        return success_response(
            data, message=ResponseMessage.OK.value, status_code=StatusCode.OK.value
        )

    except Exception as e:
        return handleError(e)


# Delete taxon
@router.delete(
    "/delete", response_model=TaxonBaseResponseModel, status_code=StatusCode.OK.value
)
async def delete_taxon_route_func(params: TaxonDeleteModel):
    try:
        data: TaxonBaseResponseModelObject = await delete_taxon(params)
        return success_response(
            data,
            message=ResponseMessage.OK_DELETE.value,
            status_code=StatusCode.OK.value,
        )

    except Exception as e:
        return handleError(e)
