from typing import List, Optional
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
    status_code: int = 200
    data: dict = {}

class PortalCreateResponseModel(ResponseBaseModel):
    status_code: int = 201
    data: List[str]

class PortalDeleteResponseModel(ResponseBaseModel):
    status_code: int = 200
    data: List[str]

class PortalGetResponseModel(ResponseBaseModel):
    status_code: int = 200
    data: List[PortalBaseModel]

class PortalDetailResponseModel(ResponseBaseModel):
    status_code: int = 200
    data: PortalBaseModel