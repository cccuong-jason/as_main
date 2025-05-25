from typing import Optional
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from langchain.llms.base import LLM

from tshirt_fulfillment.src.core.domain.agent import AgentRole
from tshirt_fulfillment.src.core.domain.agent import AgentSession
from tshirt_fulfillment.src.core.domain.agent import AgentStatus
from tshirt_fulfillment.src.core.use_cases.agent_service import AgentService


@pytest.fixture
def mock_tool_registry():
    """Mock tool registry for testing"""
    mock_registry = MagicMock()
    return mock_registry


@pytest.fixture
def order_processor(mock_order_repository):
    """Create an order processor for testing"""
    from tshirt_fulfillment.src.core.use_cases.order_processor import OrderProcessor

    return OrderProcessor(mock_order_repository)


class MockLLM(LLM):
    """Mock LLM for testing"""

    def _call(self, prompt: str, stop: Optional[list[str]] = None) -> str:
        return "Mock response"

    @property
    def _llm_type(self) -> str:
        return "mock"


@pytest.fixture
def mock_llm():
    return MockLLM()


@pytest.fixture
def agent_service(mock_llm, order_processor, mock_tool_registry, mock_design_generator):
    """Create an agent service for testing"""
    with patch("tshirt_fulfillment.src.core.use_cases.agent_service.Ollama", return_value=mock_llm):
        service = AgentService(
            order_processor=order_processor,
            design_generator=mock_design_generator,
            tool_registry=mock_tool_registry,
        )
        return service


def test_create_customer_session(agent_service, order_data):
    """Test creating a customer session"""
    # Create an order first
    order_result = agent_service.order_processor.create_order(order_data)
    assert order_result.success

    # Create customer session
    result = agent_service.create_customer_session(order_result.order.id)

    assert result.success
    assert result.session is not None
    assert result.session.role == AgentRole.CUSTOMER
    assert result.session.order_id == order_result.order.id
    assert result.session.status == AgentStatus.IDLE
    assert "executor" in result.session.context


def test_create_admin_session(agent_service):
    """Test creating an admin session"""
    command_id = "test_command_123"
    result = agent_service.create_admin_session(command_id)

    assert result.success
    assert result.session is not None
    assert result.session.role == AgentRole.ADMIN
    assert result.session.command_id == command_id
    assert result.session.status == AgentStatus.IDLE
    assert "executor" in result.session.context


def test_execute_customer_session(agent_service, order_data):
    """Test executing a customer session"""
    # Create an order first
    order_result = agent_service.order_processor.create_order(order_data)
    assert order_result.success

    # Create and execute customer session
    session_result = agent_service.create_customer_session(order_result.order.id)
    assert session_result.success

    execute_result = agent_service.execute_session(session_result.session)

    assert execute_result.success
    assert execute_result.session.status == AgentStatus.COMPLETED
    assert "result" in execute_result.session.context


def test_execute_admin_session(agent_service):
    """Test executing an admin session"""
    command_id = "test_command_123"

    # Create and execute admin session
    session_result = agent_service.create_admin_session(command_id)
    assert session_result.success

    execute_result = agent_service.execute_session(session_result.session)

    assert execute_result.success
    assert execute_result.session.status == AgentStatus.COMPLETED
    assert "result" in execute_result.session.context


def test_execute_session_with_invalid_order(agent_service):
    """Test executing a session with an invalid order ID"""
    # Create customer session with invalid order ID
    session_result = agent_service.create_customer_session("invalid_order_id")
    assert not session_result.success
    assert "Order not found" in session_result.error


def test_execute_session_without_executor(agent_service):
    """Test executing a session without an executor"""
    # Create a session without an executor
    session = AgentSession.create_customer_session("test_order_123")

    execute_result = agent_service.execute_session(session)

    assert not execute_result.success
    assert execute_result.session.status == AgentStatus.FAILED
    assert "error" in execute_result.session.context
