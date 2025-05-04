# API for T-shirt Fulfillment AI Agent

from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, Header, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn
import logging
import time
import uuid

# Import agent and configuration
from tshirt_fulfillment.core.use_cases.order_processor import TShirtFulfillmentAgent
from tshirt_fulfillment.config.settings import Config
from tshirt_fulfillment.adapters.services.admin_services import GoogleSheetAdmin

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

# Initialize AI agent
agent = TShirtFulfillmentAgent(redis_url=Config.REDIS_URL, model_name=Config.LLM_PROVIDER)

# Initialize admin tools
google_sheet_admin = GoogleSheetAdmin()

# Security - API key authentication
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In production, use a secure method to store and validate API keys
valid_api_keys = ["valid_admin_token", "test_admin_token"]

def get_api_key(api_key: str = Security(api_key_header)):
    """Validate API key for admin endpoints."""
    if api_key not in valid_api_keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
        )
    return api_key

# In-memory storage for order status (in production, use a database)
order_status = {}


# Request and response models
class OrderRequest(BaseModel):
    customer_message: str
    customer_info: Optional[Dict[str, Any]] = None
    language: str = "vi"  # Default to Vietnamese


class OrderResponse(BaseModel):
    order_id: str
    status: str
    message: str


class OrderStatusResponse(BaseModel):
    order_id: str
    status: str
    phases: List[Dict[str, Any]]
    result: Optional[Dict[str, Any]] = None


# Background task to process orders
def process_order_task(order_id: str, request: OrderRequest):
    """Background task to process an order using the AI agent."""
    try:
        # Update order status
        order_status[order_id]["status"] = "processing"
        order_status[order_id]["phases"].append({
            "phase": "processing_started",
            "timestamp": time.time(),
            "details": "Order processing started"
        })
        
        # Process the order using the AI agent
        result = agent.process_order(
            order_id=order_id,
            customer_message=request.customer_message,
            language=request.language
        )
        
        # Update order status based on result
        if result["success"]:
            order_status[order_id]["status"] = "completed"
            order_status[order_id]["phases"].append({
                "phase": "processing_completed",
                "timestamp": time.time(),
                "details": "Order processing completed successfully"
            })
        else:
            order_status[order_id]["status"] = "failed"
            order_status[order_id]["phases"].append({
                "phase": "processing_failed",
                "timestamp": time.time(),
                "details": f"Order processing failed: {result.get('error', 'Unknown error')}"
            })
        
        # Store the result
        order_status[order_id]["result"] = result
        
    except Exception as e:
        logger.error(f"Error processing order {order_id}: {str(e)}")
        order_status[order_id]["status"] = "failed"
        order_status[order_id]["phases"].append({
            "phase": "processing_error",
            "timestamp": time.time(),
            "details": f"Error: {str(e)}"
        })


# API endpoints
@app.post("/orders", response_model=OrderResponse)
async def create_order(request: OrderRequest, background_tasks: BackgroundTasks):
    """Create a new order and start processing it."""
    # Generate a unique order ID
    order_id = f"order_{uuid.uuid4().hex[:8]}_{int(time.time())}"
    
    # Initialize order status
    order_status[order_id] = {
        "status": "received",
        "phases": [{
            "phase": "order_received",
            "timestamp": time.time(),
            "details": "Order received and queued for processing"
        }],
        "result": None
    }
    
    # Start processing the order in the background
    background_tasks.add_task(process_order_task, order_id, request)
    
    return OrderResponse(
        order_id=order_id,
        status="received",
        message="Order received and processing has started"
    )


@app.get("/orders/{order_id}", response_model=OrderStatusResponse)
async def get_order_status(order_id: str):
    """Get the status of an order."""
    if order_id not in order_status:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return OrderStatusResponse(
        order_id=order_id,
        status=order_status[order_id]["status"],
        phases=order_status[order_id]["phases"],
        result=order_status[order_id]["result"]
    )


@app.post("/orders/{order_id}/approve")
async def approve_order(order_id: str):
    """Approve an order design."""
    if order_id not in order_status:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order status
    order_status[order_id]["phases"].append({
        "phase": "approval_received",
        "timestamp": time.time(),
        "details": "Customer approved the design"
    })
    
    return {"message": "Order approved successfully"}


@app.post("/orders/{order_id}/retry")
async def retry_order(order_id: str, background_tasks: BackgroundTasks):
    """Retry processing an order."""
    if order_id not in order_status:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get the original request
    original_request = OrderRequest(
        customer_message=order_status[order_id].get("customer_message", ""),
        customer_info=order_status[order_id].get("customer_info", {}),
        language=order_status[order_id].get("language", "vi")
    )
    
    # Update order status
    order_status[order_id]["status"] = "retrying"
    order_status[order_id]["phases"].append({
        "phase": "retry_started",
        "timestamp": time.time(),
        "details": "Retrying order processing"
    })
    
    # Start processing the order in the background
    background_tasks.add_task(process_order_task, order_id, original_request)
    
    return {"message": "Order processing restarted"}


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": time.time()}


# Admin API Models
class FindSheetRequest(BaseModel):
    criteria: Dict[str, Any]


class CreateSheetRequest(BaseModel):
    template_id: str
    data: Dict[str, Any]
    sheet_name: str
    share_with: List[str]


class ListFilesRequest(BaseModel):
    folder_id: Optional[str] = None
    file_type: Optional[str] = None


class SummarySheetRequest(BaseModel):
    source_sheet_ids: List[str]
    summary_name: str
    summary_type: str


# Admin API endpoints
@app.post("/admin/sheets/find", tags=["admin"])
async def find_google_sheet(request: FindSheetRequest, api_key: str = Depends(get_api_key)):
    """Find Google Sheets based on search criteria."""
    result = google_sheet_admin.find_google_sheet(
        criteria=request.criteria,
        auth_token=api_key
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/admin/sheets/create", tags=["admin"])
async def create_google_sheet(request: CreateSheetRequest, api_key: str = Depends(get_api_key)):
    """Create a new Google Sheet from a template."""
    result = google_sheet_admin.create_google_sheet_from_template(
        template_id=request.template_id,
        data=request.data,
        sheet_name=request.sheet_name,
        share_with=request.share_with,
        auth_token=api_key
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/admin/drive/list", tags=["admin"])
async def list_drive_files(request: ListFilesRequest, api_key: str = Depends(get_api_key)):
    """List files in Google Drive, optionally filtered by folder and type."""
    result = google_sheet_admin.list_drive_files(
        folder_id=request.folder_id,
        file_type=request.file_type,
        auth_token=api_key
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/admin/sheets/summary", tags=["admin"])
async def generate_summary_sheet(request: SummarySheetRequest, api_key: str = Depends(get_api_key)):
    """Generate a summary sheet from multiple source sheets."""
    result = google_sheet_admin.generate_summary_sheet(
        source_sheet_ids=request.source_sheet_ids,
        summary_name=request.summary_name,
        summary_type=request.summary_type,
        auth_token=api_key
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


# Run the API server
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)