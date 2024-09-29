from pydantic import BaseModel, Field

# Request models
class termBaseModel(BaseModel):
    species: str = Field(..., min_length=1, max_length=100)
    taxon_id: str = Field(..., min_length=1, max_length=100)
    data: dict = Field({},)

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

class searchParams(BaseModel):
    search: str = Field(..., min_length=1, max_length=500)