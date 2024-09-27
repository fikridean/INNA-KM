from typing import Optional
from pydantic import BaseModel

# Response model
class ResponseBaseModel(BaseModel):
    status_code: int
    success: bool
    message: str