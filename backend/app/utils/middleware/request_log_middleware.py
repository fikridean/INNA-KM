from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
import logging
import time
import psutil

# Create an asynchronous logger instance
requestLogger = Logger(name="request_logger")
requestLogger.level = logging.INFO

# Create an async file handler
file_handler = AsyncFileHandler("log/request.log")

# Add the file handler to the logger
requestLogger.add_handler(file_handler)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
requestLogger.formatter = formatter

# Global variables to track metrics
request_count = 0
error_count = 0


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        global request_count, error_count
        start_time = time.time()

        # System resource usage before processing the request
        cpu_usage_before = psutil.cpu_percent(interval=None)
        memory_usage_before = psutil.virtual_memory().percent

        request_count += 1

        requestLogger.info(f"Request: {request.method} {request.url}")
        requestLogger.info(f"Headers: {request.headers}")
        requestLogger.info(f"System CPU usage before request: {cpu_usage_before}%")
        requestLogger.info(
            f"System Memory usage before request: {memory_usage_before}%"
        )

        # Call the request and get the response
        try:
            response: Response = await call_next(request)

            # Capture the response size by reading it
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            response_body_size = len(response_body)

            # Create a new response using the captured body
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=response.headers,
            )

        except Exception as e:
            error_count += 1
            requestLogger.error(f"Error processing request: {e}")
            raise e

        # System resource usage after processing the request
        cpu_usage_after = psutil.cpu_percent(interval=None)
        memory_usage_after = psutil.virtual_memory().percent

        # Log the outgoing response
        end_time = time.time()
        elapsed_time = end_time - start_time

        requestLogger.info(f"Response status: {response.status_code}")
        requestLogger.info(f"Time taken: {elapsed_time:.2f} seconds")
        requestLogger.info(f"Response size: {response_body_size} bytes")
        requestLogger.info(f"System CPU usage after request: {cpu_usage_after}%")
        requestLogger.info(f"System Memory usage after request: {memory_usage_after}%")
        requestLogger.info(f"Activity: {request.method} {request.url}")
        requestLogger.info(
            f"Total Requests: {request_count}, Total Errors: {error_count}\n"
        )

        # Return the new response
        return response
