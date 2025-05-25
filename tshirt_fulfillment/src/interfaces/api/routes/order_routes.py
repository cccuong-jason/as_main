import time
import uuid
from typing import Any
from typing import Optional

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel

from tshirt_fulfillment.src.core.domain.order import Order
from tshirt_fulfillment.src.core.domain.order import OrderStatus
from tshirt_fulfillment.src.core.repositories.order_repository import OrderRepository
from tshirt_fulfillment.src.core.use_cases.order_processor import TShirtFulfillmentAgent
from tshirt_fulfillment.src.interfaces.api.dependencies import get_agent
from tshirt_fulfillment.src.interfaces.api.dependencies import get_order_repository

router = APIRouter(prefix="/orders", tags=["orders"])


# Request and response models
class OrderRequest(BaseModel):
    customer_message: str
    customer_info: Optional[dict[str, Any]] = None
    language: str = "vi"  # Default to Vietnamese


class OrderResponse(BaseModel):
    order_id: str
    status: str
    message: str


class OrderStatusResponse(BaseModel):
    order_id: str
    status: str
    phases: list[dict[str, Any]]
    result: Optional[dict[str, Any]] = None


# Background task to process orders
def process_order_task(
    order_id: str,
    request: OrderRequest,
    agent: TShirtFulfillmentAgent,
    order_repository: OrderRepository,
):
    """Background task to process an order using the AI agent."""
    try:
        # Get the order
        order = order_repository.get_by_id(order_id)
        if not order:
            return

        # Update order status
        order.status = OrderStatus.PROCESSING
        order.phases.append(
            {
                "phase": "processing_started",
                "timestamp": time.time(),
                "details": "Order processing started",
            }
        )
        order_repository.update(order)

        # Process the order using the AI agent
        result = agent.process_order(
            order_id=order_id, customer_message=request.customer_message, language=request.language
        )

        # Update order status based on result
        if result["success"]:
            order.status = OrderStatus.COMPLETED
            order.phases.append(
                {
                    "phase": "processing_completed",
                    "timestamp": time.time(),
                    "details": "Order processing completed successfully",
                }
            )
        else:
            order.status = OrderStatus.FAILED
            order.phases.append(
                {
                    "phase": "processing_failed",
                    "timestamp": time.time(),
                    "details": f"Order processing failed: {result.get('error', 'Unknown error')}",
                }
            )

        # Store the result
        order.result = result
        order_repository.update(order)

    except Exception as e:
        if order:
            order.status = OrderStatus.FAILED
            order.phases.append(
                {
                    "phase": "processing_error",
                    "timestamp": time.time(),
                    "details": f"Error: {str(e)}",
                }
            )
            order_repository.update(order)


@router.post("", response_model=OrderResponse)
async def create_order(
    request: OrderRequest,
    background_tasks: BackgroundTasks,
    agent: TShirtFulfillmentAgent = Depends(get_agent),
    order_repository: OrderRepository = Depends(get_order_repository),
):
    """Create a new order and start processing it."""
    # Generate a unique order ID
    order_id = f"order_{uuid.uuid4().hex[:8]}_{int(time.time())}"

    # Create new order
    order = Order(
        id=order_id,
        customer_message=request.customer_message,
        customer_info=request.customer_info,
        language=request.language,
        status=OrderStatus.RECEIVED,
        phases=[
            {
                "phase": "order_received",
                "timestamp": time.time(),
                "details": "Order received and queued for processing",
            }
        ],
    )

    # Save order
    order_repository.save(order)

    # Start processing the order in the background
    background_tasks.add_task(process_order_task, order_id, request, agent, order_repository)

    return OrderResponse(
        order_id=order_id, status="received", message="Order received and processing has started"
    )


@router.get("/{order_id}", response_model=OrderStatusResponse)
async def get_order_status(
    order_id: str, order_repository: OrderRepository = Depends(get_order_repository)
):
    """Get the status of an order."""
    order = order_repository.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrderStatusResponse(
        order_id=order.id, status=order.status.value, phases=order.phases, result=order.result
    )


@router.post("/{order_id}/approve")
async def approve_order(
    order_id: str, order_repository: OrderRepository = Depends(get_order_repository)
):
    """Approve an order design."""
    order = order_repository.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order status
    order.phases.append(
        {
            "phase": "approval_received",
            "timestamp": time.time(),
            "details": "Customer approved the design",
        }
    )
    order_repository.update(order)

    return {"message": "Order approved successfully"}


@router.post("/{order_id}/retry")
async def retry_order(
    order_id: str,
    background_tasks: BackgroundTasks,
    agent: TShirtFulfillmentAgent = Depends(get_agent),
    order_repository: OrderRepository = Depends(get_order_repository),
):
    """Retry processing an order."""
    order = order_repository.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Create request from order data
    request = OrderRequest(
        customer_message=order.customer_message,
        customer_info=order.customer_info,
        language=order.language,
    )

    # Update order status
    order.status = OrderStatus.RETRYING
    order.phases.append(
        {"phase": "retry_started", "timestamp": time.time(), "details": "Retrying order processing"}
    )
    order_repository.update(order)

    # Start processing the order in the background
    background_tasks.add_task(process_order_task, order_id, request, agent, order_repository)

    return {"message": "Order processing restarted"}
