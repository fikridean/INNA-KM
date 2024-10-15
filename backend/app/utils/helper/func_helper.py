import asyncio
import importlib.util
import os
from typing import List

from utils.enum.message_enum import ResponseMessage
from utils.enum.status_code_enum import StatusCode
from utils.helper.response_helper import error_response
from config import OPERATIONS_FOLDERS


def convert_to_string(obj: any) -> any:
    if isinstance(obj, dict):
        # If it's a dictionary, apply the conversion recursively to each key-value pair
        return {k: convert_to_string(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # If it's a list, apply the conversion recursively to each item in the list
        return [convert_to_string(i) for i in obj]
    else:
        # For all other data types, convert them to string
        return str(obj)


async def run_function_from_module(
    module_name: str, function_name: str, *args: any
) -> any:
    # Dynamically import the module
    spec = importlib.util.spec_from_file_location(
        module_name, OPERATIONS_FOLDERS + "/" + module_name + ".py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the function from the module
    function = getattr(module, function_name)

    if asyncio.iscoroutinefunction(function):
        # If the function is async, await it
        return await function(*args)
    else:
        # Otherwise, call the sync function directly
        return function(*args)


def get_directories(directory: str) -> int:
    try:
        # List all files in the directory
        files = os.listdir(directory)
        # Filter out directories, only count files
        files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
        return files
    except FileNotFoundError:
        print(f"The directory {directory} does not exist.")
        return 0


def find_matching_parts(data_array: list, term: str) -> list:
    results = []

    def search_dict(d):
        matched_items = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result = search_dict(value)
                if result:
                    matched_items[key] = result
            elif isinstance(value, str) and term.lower() in value.lower():
                matched_items[key] = value
        return matched_items if matched_items else None

    for data in data_array:
        # Always include 'taxon_id' and 'species' if they exist
        result = {"taxon_id": data.get("taxon_id"), "species": data.get("species")}

        matched_data = search_dict(data)
        if matched_data:
            result.update(matched_data)
        if result:
            results.append(result)

    return results


portal_webs: List[str] = [
    web.split(".")[0] for web in get_directories(OPERATIONS_FOLDERS)
]


def handleError(e: Exception):
    # Check if there are any arguments in e.args
    if len(e.args) > 0:
        error = e.args[0]

        # Check if error is a dictionary and contains the required keys
        if isinstance(error, dict) and all(
            key in error for key in ["data", "message", "status_code"]
        ):
            error_data = error["data"]
            error_message = error["message"]
            error_status_code = error["status_code"]

            return error_response(
                data=error_data, message=error_message, status_code=error_status_code
            )
        else:
            return error_response(
                data=None,
                message=ResponseMessage.ERR_INTERNAL_SERVER_ERROR.value,
                status_code=StatusCode.INTERNAL_SERVER_ERROR.value,
            )
    else:
        return error_response(
            data=None,
            message=ResponseMessage.ERR_INTERNAL_SERVER_ERROR.value,
            status_code=StatusCode.INTERNAL_SERVER_ERROR.value,
        )


# Check for unsupported web sources
def checkUnsupportedWeb(webs: List[str]) -> List[str]:
    unsupported_webs = []
    for web in webs:
        if web not in portal_webs:
            unsupported_webs.append(web)
    return unsupported_webs
