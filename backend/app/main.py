from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.middleware.request_log_middleware import RequestLoggingMiddleware
from routers import taxon_router, portal_router, raw_router, term_router
import uvicorn
from config import HOST, PORT, API_PREFIX
from prometheus_fastapi_instrumentator import Instrumentator

# Create FastAPI instance
app = FastAPI()

# Middleware registration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.add_middleware(RequestLoggingMiddleware)

# Router registration with dynamic base path
app.include_router(
    portal_router.router, prefix=f"{API_PREFIX}/portals", tags=["portals"]
)
app.include_router(raw_router.router, prefix=f"{API_PREFIX}/raws", tags=["raws"])
app.include_router(term_router.router, prefix=f"{API_PREFIX}/terms", tags=["terms"])
app.include_router(taxon_router.router, prefix=f"{API_PREFIX}/taxa", tags=["taxa"])

# Instrumentator registration
Instrumentator().instrument(app).expose(app)

# Run the app
if __name__ == "__main__":
    try:
        uvicorn.run(app, host=HOST, port=int(PORT))

    except Exception as e:
        raise Exception(f"An error occurred while running the app: {str(e)}")
