from typing import Annotated, List, Optional
from pydantic import BaseModel, Field

from models.base_custom_model import ResponseBaseModel


# Request models
class RawBaseModel(BaseModel):
    portal_id: int = Field(..., gt=0)
    web: str = Field(..., min_length=1, max_length=100)
    data: dict

    class Config:
        extra = "forbid"  # Forbid extra fields


class RawGetModel(BaseModel):
    ncbi_taxon_id: List[
        Annotated[str, Field(strict=True, min_length=1, max_length=100)]
    ]
    web: List[Annotated[str, Field(strict=True, min_length=1, max_length=100)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


class RawStoreModel(BaseModel):
    ncbi_taxon_id: List[
        Annotated[str, Field(strict=True, min_length=1, max_length=100)]
    ]
    web: List[Annotated[str, Field(strict=True, min_length=1, max_length=100)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


class RawDeleteModel(BaseModel):
    ncbi_taxon_id: List[
        Annotated[str, Field(strict=True, min_length=1, max_length=100)]
    ]
    web: List[Annotated[str, Field(strict=True, min_length=1, max_length=100)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


# Response models
class RawGetResponseModelObject(BaseModel):
    ncbi_taxon_id: Optional[str] = None
    species: Optional[str] = None
    web: Optional[str] = None
    data: Optional[dict] = None
    status: Optional[str] = None
    info: Optional[str] = None


class RawGetResponseModel(ResponseBaseModel):
    data: list[RawGetResponseModelObject]


class InFoundWebsObjectModel(BaseModel):
    web: Optional[str] = None
    status: Optional[str] = None
    info: Optional[str] = None


class FoundWebsObjectModel(BaseModel):
    exist: List[InFoundWebsObjectModel]
    not_exist: List[InFoundWebsObjectModel]


class RawStoreResponseModelObject(BaseModel):
    ncbi_taxon_id: Optional[str] = None
    species: Optional[str] = None
    found_webs: FoundWebsObjectModel
    missing_webs: Optional[List[str]] = None
    status: Optional[str] = None
    info: Optional[str] = None


class RawStoreResponseModel(ResponseBaseModel):
    data: List[RawStoreResponseModelObject]


class RawDeleteResponseModelObject(BaseModel):
    ncbi_taxon_id: Optional[str] = None
    species: Optional[str] = None
    web: Optional[str] = None
    status: Optional[str] = None
    info: Optional[str] = None


class RawDeleteResponseModel(BaseModel):
    data: List[RawDeleteResponseModelObject]
