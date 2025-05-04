# Test fixtures for integration tests
import pytest
from unittest.mock import MagicMock
from tshirt_fulfillment.core.domain.order import Order
from tshirt_fulfillment.core.domain.design import Design
from tshirt_fulfillment.core.use_cases.order_processor import OrderProcessor
from tshirt_fulfillment.core.use_cases.design_generator import DesignGenerator

# Import fixtures from the main conftest.py
pytestmark = pytest.mark.usefixtures("order_data", "design_data", "mock_order_repository", "mock_llm_service")

@pytest.fixture
def integrated_order_processor(mock_order_repository, mock_design_repository, mock_llm_service):
    """Create an order processor with real dependencies for integration testing"""
    design_generator = DesignGenerator(
        design_repository=mock_design_repository,
        llm_service=mock_llm_service
    )
    
    return OrderProcessor(
        order_repository=mock_order_repository,
        design_generator=design_generator
    )

@pytest.fixture
def sample_order(order_data):
    """Create a sample order for integration tests"""
    return Order(**order_data)

@pytest.fixture
def sample_design(design_data):
    """Create a sample design for integration tests"""
    return Design(**design_data)

@pytest.fixture
def db_session():
    """Create a test database session"""
    # This would typically set up a test database connection
    # For now, we'll just use a mock
    session = MagicMock()
    yield session
    # Clean up after the test
    session.close()

@pytest.fixture
def api_client():
    """Create a test API client"""
    # This would typically set up a test client for the API
    # For now, we'll just use a mock
    from fastapi.testclient import TestClient
    from tshirt_fulfillment.interfaces.api.fastapi_app import app
    
    client = TestClient(app)
    return client