from typing import Optional
from pydantic import BaseModel


# Response model
class ResponseBaseModel(BaseModel):
    status_code: int = 200
    success: bool = True
    message: str = "Success"
    total_data: Optional[int]
