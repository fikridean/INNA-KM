from pydantic import BaseModel, Field

# Request models
class TermGetModel(BaseModel):
    taxon_id: list[str]

    class Config:
        extra = "forbid"  # Forbid extra fields

class TermStoreModel(BaseModel):
    taxon_id: list[str]

    class Config:
        extra = "forbid"  # Forbid extra fields

class TermDeleteModel(BaseModel):
    taxon_id: list[str]

    class Config:
        extra = "forbid"  # Forbid extra fields

class searchModel(BaseModel):
    search: str = Field(..., min_length=1, max_length=500)

# Response models
class TermGetResponseModel(BaseModel):
    taxon_id: str
    species: str
    data: dict
    status: str
    info: str

class TermStoreResponseModel(BaseModel):
    taxon_id: str
    species: str
    data: dict
    status: str
    info: str

class TermDeleteResponseModel(BaseModel):
    taxon_id: str
    species: str
    status: str
    info: str

class searchResponseModel(BaseModel):
    taxon_id: str
    species: str
    data: dict
    status: str
    info: str