from functools import wraps
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
from aiologger.handlers.streams import AsyncStreamHandler
import logging
from datetime import datetime as time
from config import DEBUG

# Create an asynchronous logger instance
appLogger = Logger(name="app_logger")
appLogger.level = logging.INFO  # Set the log level for the logger

# Create an async file handler
file_handler = AsyncFileHandler("app/log/app.log")  # Specify your log file

# Create a console handler
# console_handler = AsyncStreamHandler()

# Add the file handler to the logger
appLogger.add_handler(file_handler)
# appLogger.add_handler(console_handler)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set the formatter to the logger (not the handler)
appLogger.formatter = formatter

def log_function(action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:

                if DEBUG == True:
                    # Log function entry
                    appLogger.info(f"Entering {action} with args: {args}, kwargs: {kwargs}")
                    start_time = time.utcnow()
                    
                # Call the actual function
                result = await func(*args, **kwargs)
                    
                if DEBUG == True:
                    # Log function exit
                    elapsed_time = time.utcnow() - start_time
                    appLogger.info(f"Exiting {action} with result: {result}, took {elapsed_time}\n")
                    
                
                return result
            except Exception as e:
                # Log exceptions
                appLogger.error(f"Error in {action}: {str(e)}\n")
                raise e
        return wrapper
    return decorator