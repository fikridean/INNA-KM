import asyncio
import importlib.util
import os

from config import OPERATIONS_FOLDERS

def convert_to_string(obj: any) -> any:
    try:
        if isinstance(obj, dict):
            # If it's a dictionary, apply the conversion recursively to each key-value pair
            return {k: convert_to_string(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # If it's a list, apply the conversion recursively to each item in the list
            return [convert_to_string(i) for i in obj]
        else:
            # For all other data types, convert them to string
            return str(obj)
        
    except Exception as e:
        raise Exception(f"An error occurred while converting to string: {str(e)}")

async def run_function_from_module(module_name: str, function_name: str, *args: any) -> any:
    try:
        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(module_name, OPERATIONS_FOLDERS + '/' + module_name + ".py")
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
        
    except Exception as e:
        raise Exception(f"An error occurred while running function from module: {str(e)}")
    
def get_portals_webs(directory: str) -> int:
    try:
        # List all files in the directory
        files = os.listdir(directory)
        # Filter out directories, only count files
        files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
        return files
    except FileNotFoundError:
        print(f"The directory {directory} does not exist.")
        return 0

def find_matching_parts(data_array, term):
    try:

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
            # Always include 'web' and 'species' if they exist
            result = {'web': data.get('web'), 'species': data.get('species')}
            matched_data = search_dict(data)
            if matched_data:
                result.update(matched_data)
            if result:
                results.append(result)
        
        return results
    
    except Exception as e:
        raise Exception(f"An error occurred while finding matching parts: {str(e)}")
    
