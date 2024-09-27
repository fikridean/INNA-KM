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
    status_code: int = 200
    data: list[RawBaseModel]

class DataStoredObjectModel(BaseModel):
    total_data: int
    data: list[str]

class DataNotStoredObjectModel(DataStoredObjectModel):
    note: str

class RawStoreObjectModel(BaseModel):
    total_portal_found: int
    data_stored: DataStoredObjectModel
    data_not_stored: DataNotStoredObjectModel

class RawStoreResponseModel(BaseModel):
    status_code: int = 200
    data: DataStoredObjectModel

class RawDeleteResponseModel(BaseModel):
    status_code: int = 200
    data: DataStoredObjectModel