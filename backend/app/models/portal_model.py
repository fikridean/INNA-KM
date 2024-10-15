from typing import Annotated, List, Optional
from pydantic import BaseModel, Field

from models.base_custom_model import ResponseBaseModel


# Request models
class PortalBaseModel(BaseModel):
    portal_id: int = Field(..., gt=0)
    taxon_id: str = Field(..., min_length=1, max_length=100)
    web: str = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields


class PortalCreateModel(BaseModel):
    portal_id: int = Field(..., gt=0)
    taxon_id: int = Field(..., gt=0)
    web: List[Annotated[str, Field(strict=True, min_length=1, max_length=100)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


class PortalGetModel(BaseModel):
    portal_id: List[Annotated[int, Field(strict=True, gt=0)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


class PortalDetailModel(BaseModel):
    portal_id: int = Field(..., gt=0)

    class Config:
        extra = "forbid"  # Forbid extra fields


class PortalDeleteModel(BaseModel):
    portal_id: List[Annotated[int, Field(strict=True, gt=0)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


class PortalRetrieveDataModel(BaseModel):
    ncbi_taxon_id: str = Field(..., min_length=1, max_length=100)
    web: str = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields


# Response models
class PortalCreateResponseModelObject(BaseModel):
    portal_id: Optional[int] = None
    taxon_id: Optional[int] = None
    web: Optional[List[str]] = None
    status: Optional[str] = None
    info: Optional[str] = None


class PortalCreateResponseModel(ResponseBaseModel):
    data: List[PortalCreateResponseModelObject]


class PortalGetResponseModelObject(BaseModel):
    portal_id: Optional[int] = None
    taxon_id: Optional[int] = None
    web: Optional[List[str]] = None
    status: Optional[str] = None
    info: Optional[str] = None


class PortalGetResponseModel(ResponseBaseModel):
    data: List[PortalGetResponseModelObject]


class PortalDetailResponseModelObject(BaseModel):
    portal_id: Optional[int] = None
    taxon_id: Optional[int] = None
    web: Optional[List[str]] = None
    status: Optional[str] = None
    info: Optional[str] = None


class PortalDetailResponseModel(ResponseBaseModel):
    data: PortalDetailResponseModelObject


class PortalDeleteResponseModelObject(BaseModel):
    portal_id: Optional[int] = None
    taxon_id: Optional[int] = None
    web: Optional[List[str]] = None
    status: Optional[str] = None
    info: Optional[str] = None


class PortalDeleteResponseModel(ResponseBaseModel):
    data: List[PortalDeleteResponseModelObject]


class PortalRetrieveDataResponseModelObject(BaseModel):
    portal_id: Optional[int] = None
    taxon_id: Optional[int] = None
    web: Optional[str] = None
    data: Optional[dict] = None
    status: Optional[str] = None
    info: Optional[str] = None


class PortalRetrieveDataResponseModel(ResponseBaseModel):
    data: PortalRetrieveDataResponseModelObject
