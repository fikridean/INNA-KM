from fastapi.responses import JSONResponse
from typing import Any


def success_response(
    data: Any, message: str = "Operation successful", status_code: int = 200
) -> JSONResponse:
    content = {
        "status": status_code,
        "success": True,
        "message": message,
    }

    # Handle list of Pydantic models or dicts
    if isinstance(data, list):
        # Convert list of Pydantic models to list of dicts
        content["total_data"] = len(data)
        content["data"] = [
            item.dict() if hasattr(item, "dict") else item for item in data
        ]

    # Handle a single Pydantic model or dict
    elif isinstance(data, dict) or hasattr(data, "dict"):
        content["total_data"] = 1
        content["data"] = data.dict() if hasattr(data, "dict") else data

    # Handle None or empty data
    else:
        content["total_data"] = 0
        content["data"] = []

    return JSONResponse(content=content)


def error_response(
    data: Any = None, message: str = "An error occurred", status_code: int = 400
) -> JSONResponse:
    return JSONResponse(
        content={
            "status": status_code,
            "success": False,
            "message": message,
            "total_data": 0,
            "data": data,
        }
    )
