# Order processing use case

from typing import Dict, Any, Optional
from dataclasses import dataclass

from tshirt_fulfillment.core.domain.order import Order
from tshirt_fulfillment.core.domain.design import Design


@dataclass
class OrderProcessingResult:
    """Result of order processing operations"""
    success: bool
    order: Optional[Order] = None
    design: Optional[Design] = None
    error: Optional[str] = None


class OrderProcessor:
    """Use case for processing T-shirt orders.
    
    This class implements the business logic for order processing,
    including order creation, validation, and fulfillment.
    """
    
    def __init__(self, order_repository, design_generator=None, llm_service=None):
        """Initialize the order processor use case.
        
        Args:
            order_repository: Repository for order persistence
            design_generator: Service for generating designs
            llm_service: Optional LLM service for advanced processing
        """
        self.order_repository = order_repository
        self.design_generator = design_generator
        self.llm_service = llm_service
    
    def create_order(self, order_data: Dict[str, Any]) -> OrderProcessingResult:
        """Create a new order.
        
        Args:
            order_data: Dictionary containing order information
            
        Returns:
            OrderProcessingResult with success status and order
        """
        try:
            # Create order domain entity
            order = Order(**order_data)
            
            # Save to repository
            saved_order = self.order_repository.save(order)
            
            return OrderProcessingResult(
                success=True,
                order=saved_order
            )
        except Exception as e:
            return OrderProcessingResult(
                success=False,
                error=str(e)
            )
    
    def process_order(self, order_id: str) -> OrderProcessingResult:
        """Process an existing order.
        
        Args:
            order_id: ID of the order to process
            
        Returns:
            OrderProcessingResult with success status, order and design
        """
        try:
            # Retrieve order
            order = self.order_repository.get_by_id(order_id)
            if not order:
                return OrderProcessingResult(
                    success=False,
                    error=f"Order with ID {order_id} not found"
                )
            
            # Update order status
            from tshirt_fulfillment.core.domain.order import OrderStatus
            order.update_status(OrderStatus.PROCESSING)
            # No need to save again as the repository already has this order
            
            # Generate design if design generator is available
            design = None
            if self.design_generator:
                design_result = self.design_generator.generate_design(
                    order_id=order.id,
                    prompt=order.customer_message
                )
                
                if design_result.get("success"):
                    # Create design entity
                    from tshirt_fulfillment.core.domain.design import DesignProvider
                    design = Design.create(
                        order_id=order.id,
                        prompt=order.customer_message,
                        provider=DesignProvider.MOCK
                    )
                    design.set_result(
                        image_path=design_result.get("image_path", ""),
                        generation_time=1.0  # Default generation time
                    )
            
            return OrderProcessingResult(
                success=True,
                order=order,
                design=design
            )
        except Exception as e:
            return OrderProcessingResult(
                success=False,
                error=str(e)
            )
    
    def get_order(self, order_id: str) -> OrderProcessingResult:
        """Get an order by ID.
        
        Args:
            order_id: ID of the order to retrieve
            
        Returns:
            OrderProcessingResult with success status and order
        """
        try:
            order = self.order_repository.get_by_id(order_id)
            if not order:
                return OrderProcessingResult(
                    success=False,
                    error=f"Order with ID {order_id} not found"
                )
            
            return OrderProcessingResult(
                success=True,
                order=order
            )
        except Exception as e:
            return OrderProcessingResult(
                success=False,
                error=str(e)
            )