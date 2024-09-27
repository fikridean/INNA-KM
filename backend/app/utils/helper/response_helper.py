from fastapi.responses import JSONResponse
from typing import Any

def success_response(data: Any, message: str = "Operation successful", status_code: int = 200) -> JSONResponse:
    content = {
        "status": status_code,
        "success": True,
        "message": message,
    }

    # Check if data is a list
    if isinstance(data, list):
        content["total_data"] = len(data)

    # Append data to content for last item
    content["data"] = data

    return JSONResponse(
        content=content
    )

def error_response(message: str = "An error occurred", status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        content={
            "status": status_code,
            "success": False,
            "message": message,
            "total_data": None,
            "data": None
        }
    )