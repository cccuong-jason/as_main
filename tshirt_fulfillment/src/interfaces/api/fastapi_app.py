# API for T-shirt Fulfillment AI Agent

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from tshirt_fulfillment.src.config.settings import Config
from tshirt_fulfillment.src.interfaces.api.routes import order_routes, admin_routes

# Set up logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="T-shirt Fulfillment AI Agent API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(order_routes.router)
app.include_router(admin_routes.router)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)