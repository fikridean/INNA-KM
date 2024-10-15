from typing import Annotated, List, Optional
from pydantic import BaseModel, Field

from models.base_model import ResponseBaseModel
# Request models
class TaxonBaseModel(BaseModel):
    taxon_id: int = Field(..., ge=1)
    ncbi_taxon_id: str = Field(..., min_length=1, max_length=100)
    species: str = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields

class TaxonGetModel(BaseModel):
    taxon_id: List[Annotated[int, Field(..., ge=1)]]

    class Config:
        extra = "forbid"  # Forbid extra fields

class TaxonGetDetailModel(BaseModel):
    taxon_id: int = Field(..., ge=1)

    class Config:
        extra = "forbid"  # Forbid extra fields

class TaxonDeleteModel(BaseModel):
    taxon_id: List[Annotated[int, Field(..., ge=1)]]

    class Config:
        extra = "forbid"  # Forbid extra fields

# Response models
class TaxonBaseResponseModelObject(BaseModel):
    taxon_id: Optional[int] = None
    ncbi_taxon_id: Optional[str] = None
    species: Optional[str] = None
    status: Optional[str] = None
    info: Optional[str] = None

class TaxonBaseResponseModel(ResponseBaseModel):
    data: List[TaxonBaseResponseModelObject]

class TaxonGetResponseModelObject(BaseModel):
    taxon_id: Optional[int] = None
    ncbi_taxon_id: Optional[str] = None
    species: Optional[str] = None
    status: Optional[str] = None
    info: Optional[str] = None

class TaxonGetResponseModel(ResponseBaseModel):
    data: List[TaxonGetResponseModelObject]

class TaxonGetDetailResponseModel(ResponseBaseModel):
    data: TaxonGetResponseModelObject