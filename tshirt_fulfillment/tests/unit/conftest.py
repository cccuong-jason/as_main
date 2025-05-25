# Test fixtures and configuration for pytest
import pytest
import os
import sys
from unittest.mock import MagicMock

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# =============================================================================
# Common Fixtures for All Test Types
# =============================================================================

# Data Fixtures
@pytest.fixture
def order_data():
    """Sample order data for testing"""
    return {
        "id": "order123",
        "customer_name": "Test Customer",
        "customer_email": "test@example.com",
        "design_prompt": "A t-shirt with a mountain landscape",
        "size": "L",
        "color": "Blue",
        "quantity": 1,
        "status": "pending",
        "customer_message": "A t-shirt with a mountain landscape",
        "language": "en"
    }

@pytest.fixture
def design_data():
    """Sample design data for testing"""
    return {
        "id": "design123",
        "prompt": "A t-shirt with a mountain landscape",
        "image_url": "https://example.com/image.png",
        "status": "completed"
    }

@pytest.fixture
def admin_data():
    """Sample admin data for testing"""
    return {
        "id": "admin123",
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin"
    }

# =============================================================================
# Mock Repositories
# =============================================================================

@pytest.fixture
def mock_order_repository():
    """Mock for order repository"""
    class MockOrderRepository:
        def __init__(self):
            self.orders = {}
        
        def save(self, order):
            # Check for duplicate IDs using either id or order_id attribute
            order_id = getattr(order, 'id', None) or getattr(order, 'order_id', None)
            if order_id in self.orders:
                raise ValueError("Order with this ID already exists")
            self.orders[order_id] = order
            return order
        
        def get_by_id(self, order_id):
            return self.orders.get(order_id)
        
        def get_all(self):
            return list(self.orders.values())
        
        def update(self, order):
            order_id = getattr(order, 'id', None) or getattr(order, 'order_id', None)
            if order_id not in self.orders:
                raise ValueError("Order not found")
            self.orders[order_id] = order
            return order
        
        def delete(self, order_id):
            if order_id not in self.orders:
                raise ValueError("Order not found")
            del self.orders[order_id]
    
    return MockOrderRepository()

@pytest.fixture
def mock_design_repository():
    """Mock for design repository"""
    class MockDesignRepository:
        def __init__(self):
            self.designs = {}
        
        def save(self, design):
            if design.id in self.designs:
                raise ValueError("Design with this ID already exists")
            self.designs[design.id] = design
            return design
        
        def get_by_id(self, design_id):
            return self.designs.get(design_id)
        
        def get_all(self):
            return list(self.designs.values())
        
        def update(self, design):
            if design.id not in self.designs:
                raise ValueError("Design not found")
            self.designs[design.id] = design
            return design
        
        def delete(self, design_id):
            if design_id not in self.designs:
                raise ValueError("Design not found")
            del self.designs[design_id]
    
    return MockDesignRepository()

# =============================================================================
# Mock External Services
# =============================================================================

@pytest.fixture
def mock_llm_service():
    """Mock for LLM service"""
    from unittest.mock import MagicMock
    
    mock_service = MagicMock()
    
    # Set up default return values
    mock_service.generate_design.return_value = "https://example.com/generated_image.png"
    mock_service.enhance_prompt.return_value = "Enhanced: test prompt"
    
    # Set up generate_image method with proper mocking
    mock_service.generate_image.return_value = {
        "success": True,
        "image_path": "https://example.com/generated_image.png",
        "prompt": "test prompt"
    }
    
    # Set up generate method to use generate_image
    mock_service.generate.return_value = mock_service.generate_image.return_value
    
    return mock_service
    
    return MockLLMService()

@pytest.fixture
def mock_payment_service():
    """Mock for payment service"""
    class MockPaymentService:
        def process_payment(self, amount, payment_details):
            return {
                "success": True,
                "transaction_id": "txn_123456",
                "amount": amount
            }
        
        def refund_payment(self, transaction_id):
            return {
                "success": True,
                "refund_id": "ref_123456",
                "transaction_id": transaction_id
            }
    
    return MockPaymentService()

@pytest.fixture
def mock_email_service():
    """Mock for email service"""
    class MockEmailService:
        def __init__(self):
            self.sent_emails = []
        
        def send_email(self, to, subject, body):
            self.sent_emails.append({
                "to": to,
                "subject": subject,
                "body": body
            })
            return True
    
    return MockEmailService()