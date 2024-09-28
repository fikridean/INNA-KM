from pydantic import BaseModel, Field

class termBaseModel(BaseModel):
    species: str = Field(..., min_length=1, max_length=100)
    taxon_id: str = Field(..., min_length=1, max_length=100)
    data: dict = Field({},)

class ListOfParams(BaseModel):
    species: list = []

class TermGetModel(BaseModel):
    species: list[str]

    class Config:
        extra = "forbid"  # Forbid extra fields

class TermStoreModel(BaseModel):
    taxon_id: str = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields

class TermDeleteModel(BaseModel):
    species: list[str] = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields
        
class TermStoreFromRawModel(BaseModel):
    species: list[str] = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"  # Forbid extra fields

class searchParams(BaseModel):
    search: str = Field(..., min_length=1, max_length=500)