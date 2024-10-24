from typing import Annotated, List, Optional
from pydantic import BaseModel, Field

from models.base_custom_model import ResponseBaseModel


# Request models
class TermGetModel(BaseModel):
    ncbi_taxon_id: List[Annotated[str, Field(..., min_length=1, max_length=100)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


class TermStoreModel(BaseModel):
    ncbi_taxon_id: List[Annotated[str, Field(..., min_length=1, max_length=100)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


class TermDeleteModel(BaseModel):
    ncbi_taxon_id: List[Annotated[str, Field(..., min_length=1, max_length=100)]]

    class Config:
        extra = "forbid"  # Forbid extra fields


class searchModel(BaseModel):
    search: str = Field(..., min_length=1, max_length=500)


# Response models
class TermStoreResponseModelObject(BaseModel):
    taxon_id: Optional[int] = Field(None, ge=1)
    ncbi_taxon_id: Optional[str] = Field(None, min_length=1, max_length=100)
    species: Optional[str] = Field(None, min_length=1, max_length=100)
    data: Optional[dict] = Field(None)
    status: Optional[str] = None
    info: Optional[str] = None


class TermStoreResponseModel(ResponseBaseModel):
    data: List[TermStoreResponseModelObject]


class TermGetResponseModelObject(BaseModel):
    taxon_id: Optional[int] = Field(None, ge=1)
    ncbi_taxon_id: Optional[str] = Field(None, min_length=1, max_length=100)
    species: Optional[str] = Field(None, min_length=1, max_length=100)
    data: Optional[dict] = Field(None)
    status: Optional[str] = None
    info: Optional[str] = None


class TermGetResponseModel(ResponseBaseModel):
    data: List[TermGetResponseModelObject]


class TermDeleteResponseModelObject(BaseModel):
    taxon_id: Optional[int] = Field(None, ge=1)
    ncbi_taxon_id: Optional[str] = Field(None, min_length=1, max_length=100)
    species: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = Field(None, min_length=1, max_length=100)
    info: Optional[str] = Field(None, min_length=1, max_length=100)


class TermDeleteResponseModel(ResponseBaseModel):
    data: List[TermDeleteResponseModelObject]


class searchResponseModelObject(BaseModel):
    taxon_id: Optional[str] = Field(None, min_length=1, max_length=100)
    species: Optional[str] = Field(None, min_length=1, max_length=100)
    data: Optional[dict] = Field(None)


class searchResponseModel(ResponseBaseModel):
    data: List[searchResponseModelObject]
