from typing import List
from pydantic import BaseModel, Field

from models.base_model import ResponseBaseModel

# Request models
class PortalBaseModel(BaseModel):
    species: str = Field(..., min_length=1, max_length=100)
    taxon_id: str = Field(..., min_length=1, max_length=100)
    web: str = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields

class PortalGetModel(BaseModel):
    taxon_id: list[str]
    web: list[str]

    class Config:
        extra = "forbid"  # Forbid extra fields

class PortalDeleteModel(BaseModel):
    taxon_id: list[str] = Field(..., min_length=1, max_length=100)
    web: list[str] = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields

class PortalRetrieveDataModel(BaseModel):
    taxon_id: str = Field(..., min_length=1, max_length=100)
    web: str = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields

class PortalDetailModel(BaseModel):
    taxon_id: str = Field(..., min_length=1, max_length=100)
    web: str = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields

# Response models
class PortalRetrieveDataResponseModel(ResponseBaseModel):
    data: dict = {}

class PortalCreateResponseObjectModel(BaseModel):
    species: str
    taxon_id: str
    webs: List[str]
    status: str
    info: str

class PortalCreateResponseModel(ResponseBaseModel):
    data: List[PortalCreateResponseObjectModel]

class PortalDeleteResponseObjectModel(BaseModel):
    taxon_id: str
    species: str
    found_webs: List[str]
    missing_webs: List[str]
    status: str
    info: str

class PortalDeleteResponseModel(ResponseBaseModel):
    data: List[PortalDeleteResponseObjectModel]

class PortalGetResponseModel(ResponseBaseModel):
    data: List[PortalBaseModel]

class PortalGetWithDetailWebObjectModel(BaseModel):
    taxon_id: str
    species: str
    found_webs: List[str]
    missing_webs: List[str]
    status: str
    info: str

class PortalGetWithDetailWebResponseModel(ResponseBaseModel):
    data: List[PortalGetWithDetailWebObjectModel]

class PortalDetailResponseModel(ResponseBaseModel):
    data: PortalBaseModel