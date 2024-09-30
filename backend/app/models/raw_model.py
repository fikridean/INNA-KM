from typing import List
from pydantic import BaseModel, Field

# Request models
class RawBaseModel(BaseModel):
    taxon_id: str = Field(..., min_length=1, max_length=100)
    species: str = Field(..., min_length=1, max_length=100)
    web: str = Field(..., min_length=1, max_length=100)
    data: dict

    class Config:
        extra = "forbid"  # Forbid extra fields

class RawGetModel(BaseModel):
    taxon_id: list[str]
    web: list[str]

    class Config:
        extra = "forbid"  # Forbid extra fields

class RawStoreModel(BaseModel):
    taxon_id: list[str] 
    web: list[str]

    class Config:
        extra = "forbid"  # Forbid extra fields

class RawDeleteModel(BaseModel):
    taxon_id: list[str] 
    web: list[str]

    class Config:
        extra = "forbid"  # Forbid extra fields

# Response models
class RawGetResponseModel(BaseModel):
    data: list[RawBaseModel]

class RawGetWithWebDetailResponseModel(BaseModel):
    taxon_id: str
    species: str
    found_webs: dict
    missing_webs: List[str]
    status: str
    info: str

class InFoundWebsObjectModel(BaseModel):
    web: str
    status: str
    info: str

class FoundWebsObjectModel(BaseModel):
    exist: List[InFoundWebsObjectModel]
    not_exist: List[InFoundWebsObjectModel]

class RawStoreObjectModel(BaseModel):
    taxon_id: str
    species: str
    found_webs: FoundWebsObjectModel
    missing_webs: List[str]

class RawStoreResponseModel(BaseModel):
    data: List[RawStoreObjectModel]

class RawDeleteResponseObjectModel(BaseModel):
    taxon_id: str
    species: str
    found_webs: List[str]
    missing_webs: List[str]
    status: str
    info: str

class RawDeleteResponseModel(BaseModel):
    data: List[RawDeleteResponseObjectModel]