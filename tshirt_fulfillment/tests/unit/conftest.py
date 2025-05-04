# Test fixtures for unit tests
import pytest
from unittest.mock import MagicMock

# Import fixtures from the main conftest.py
pytestmark = pytest.mark.usefixtures("order_data", "design_data")

@pytest.fixture
def mock_design_repository():
    """Mock for design repository"""
    class MockDesignRepository:
        def __init__(self):
            self.designs = {}
        
        def save(self, design):
            self.designs[design.order_id] = design
            return design
        
        def get_by_id(self, design_id):
            return self.designs.get(design_id)
        
        def get_all(self):
            return list(self.designs.values())
    
    return MockDesignRepository()

@pytest.fixture
def mock_design_service():
    """Mock for design service"""
    class MockDesignService:
        def generate_image(self, prompt):
            return "https://example.com/generated_image.png"
    
    return MockDesignService()

@pytest.fixture
def mock_design_generator(mock_design_repository, mock_llm_service):
    """Mock for design generator"""
    from tshirt_fulfillment.core.use_cases.design_generator import DesignGenerator
    
    design_generator = DesignGenerator(
        design_repository=mock_design_repository,
        llm_service=mock_llm_service
    )
    
    # Mock the generate_design method to return a predictable result
    original_generate_design = design_generator.generate_design
    
    def mock_generate_design(order_id, prompt, style=None):
        result = original_generate_design(order_id, prompt, style)
        return result
    
    design_generator.generate_design = mock_generate_design
    return design_generator

@pytest.fixture
def mock_admin_service():
    """Mock for admin service"""
    class MockAdminService:
        def create_report(self, start_date, end_date):
            return {
                "total_orders": 10,
                "completed_orders": 8,
                "pending_orders": 2,
                "revenue": 500.00
            }
    
    return MockAdminService()

@pytest.fixture
def mock_llm_service():
    """Mock for LLM service"""
    class MockLLMService:
        def generate_image(self, prompt):
            return "https://example.com/generated_image.png"
        
        def enhance_prompt(self, prompt):
            return f"Enhanced: {prompt}"
    
    return MockLLMService()