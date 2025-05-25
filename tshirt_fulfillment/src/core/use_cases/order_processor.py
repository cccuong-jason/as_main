"""Order processing use case implementation."""
import logging
from dataclasses import dataclass
from typing import Any
from typing import Optional

import requests

from tshirt_fulfillment.src.config.settings import Config
from tshirt_fulfillment.src.core.domain.design import Design
from tshirt_fulfillment.src.core.domain.order import Order
from tshirt_fulfillment.src.core.domain.order import OrderStatus

logger = logging.getLogger(__name__)


@dataclass
class OrderProcessingResult:
    """Result of order processing operations"""

    success: bool
    order: Optional[Order] = None
    orders: Optional[list[Order]] = None
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

    def create_order(self, order_data: dict[str, Any]) -> OrderProcessingResult:
        """Create a new order.

        Args:
            order_data: Dictionary containing order information

        Returns:
            OrderProcessingResult with success status and order
        """
        try:
            # Validate customer_name
            customer_name = order_data.get("customer_name")
            if not customer_name or not customer_name.strip():
                return OrderProcessingResult(
                    success=False, error="Validation error: Customer name cannot be empty"
                )
            # Create order domain entity
            order = Order(**order_data)

            # Save to repository
            saved_order = self.order_repository.save(order)

            return OrderProcessingResult(success=True, order=saved_order)
        except Exception as e:
            return OrderProcessingResult(success=False, error=str(e))

    def process_order(self, order_id: str) -> OrderProcessingResult:
        """Process an existing order.

        Args:
            order_id: ID of the order to process

        Returns:
            OrderProcessingResult with success status and updated order
        """
        try:
            # Get order
            order = self.order_repository.get_by_id(order_id)
            if not order:
                return OrderProcessingResult(success=False, error=f"Order not found: {order_id}")

            # Generate design
            design_result = self.design_generator.generate_design(
                order_id=order.id, prompt=order.customer_message
            )

            if not design_result.success:
                return OrderProcessingResult(
                    success=False,
                    order=order,
                    error=f"Design generation failed: {design_result.error}",
                )

            # Update order status
            order.update_status(OrderStatus.PROCESSING)
            self.order_repository.update(order)

            return OrderProcessingResult(success=True, order=order, design=design_result.design)

        except Exception as e:
            return OrderProcessingResult(success=False, error=str(e))

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
                    success=False, error=f"Order with ID {order_id} not found"
                )

            return OrderProcessingResult(success=True, order=order)
        except Exception as e:
            return OrderProcessingResult(success=False, error=str(e))

    def get_all_orders(self) -> OrderProcessingResult:
        """Get all orders in the system."""
        try:
            orders = self.order_repository.get_all()
            return OrderProcessingResult(success=True, orders=orders)
        except Exception as e:
            return OrderProcessingResult(success=False, error=str(e))


class TShirtFulfillmentAgent:
    """AI agent for processing T-shirt orders."""

    def __init__(self, redis_url: str, model_name: str):
        """Initialize the agent.

        Args:
            redis_url: URL for Redis connection
            model_name: Name of the LLM model to use
        """
        self.redis_url = redis_url
        self.model_name = model_name
        self.ollama_base_url = Config.OLLAMA_BASE_URL
        self.max_iterations = Config.MAX_AGENT_ITERATIONS

    def process_order(
        self, order_id: str, customer_message: str, language: str = "vi"
    ) -> dict[str, Any]:
        """Process a T-shirt order using AI.

        Args:
            order_id: Unique identifier for the order
            customer_message: Customer's order description
            language: Language code for the order (default: "vi")

        Returns:
            Dict containing processing results
        """
        try:
            # Initialize conversation with the LLM
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a T-shirt design assistant. "
                        "Help customers create their T-shirt designs based on their "
                        "descriptions. Ask clarifying questions if needed."
                    ),
                },
                {"role": "user", "content": customer_message},
            ]

            # Get initial response from LLM
            response = self._call_llm(messages)
            if not response:
                return {"success": False, "error": "Failed to get response from LLM"}

            # Process the response and generate design
            design_result = self._generate_design(response)
            if not design_result["success"]:
                return design_result

            return {
                "success": True,
                "order_id": order_id,
                "design": design_result["design"],
                "conversation": messages + [{"role": "assistant", "content": response}],
            }

        except Exception as e:
            logger.error(f"Error processing order {order_id}: {str(e)}")
            return {"success": False, "error": f"Error processing order: {str(e)}"}

    def _call_llm(self, messages: list) -> Optional[str]:
        """Call the LLM API.

        Args:
            messages: List of conversation messages

        Returns:
            LLM response text or None if failed
        """
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={"model": self.model_name, "messages": messages, "stream": False},
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            return None

    def _generate_design(self, description: str) -> dict[str, Any]:
        """Generate a T-shirt design based on the description.

        Args:
            description: Design description from LLM

        Returns:
            Dict containing design generation results
        """
        try:
            # For now, return a placeholder design
            # TODO: Implement actual design generation
            return {
                "success": True,
                "design": {
                    "description": description,
                    "image_url": "placeholder.jpg",
                    "metadata": {"style": "placeholder", "colors": ["#000000"], "size": "M"},
                },
            }
        except Exception as e:
            logger.error(f"Error generating design: {str(e)}")
            return {"success": False, "error": f"Error generating design: {str(e)}"}
