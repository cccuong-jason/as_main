from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import uuid


class AgentRole(Enum):
    """Enum representing the possible roles of the AI agent."""
    CUSTOMER = "customer"
    ADMIN = "admin"


class AgentStatus(Enum):
    """Enum representing the possible statuses of the AI agent."""
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ToolCall:
    """Represents a tool call made by the agent."""
    tool_name: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    success: bool
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


@dataclass
class AgentSession:
    """Domain entity representing an AI agent session."""
    id: str
    role: AgentRole
    status: AgentStatus
    order_id: Optional[str] = None
    command_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    tool_history: List[ToolCall] = field(default_factory=list)
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    updated_at: float = field(default_factory=lambda: datetime.now().timestamp())

    @classmethod
    def create_customer_session(cls, order_id: str) -> 'AgentSession':
        """Create a new customer session for order processing."""
        return cls(
            id=str(uuid.uuid4()),
            role=AgentRole.CUSTOMER,
            status=AgentStatus.IDLE,
            order_id=order_id
        )

    @classmethod
    def create_admin_session(cls, command_id: str) -> 'AgentSession':
        """Create a new admin session for command processing."""
        return cls(
            id=str(uuid.uuid4()),
            role=AgentRole.ADMIN,
            status=AgentStatus.IDLE,
            command_id=command_id
        )

    def add_tool_call(self, tool_name: str, input_data: Dict[str, Any], 
                     output_data: Dict[str, Any], success: bool) -> None:
        """Add a tool call to the session history."""
        self.tool_history.append(ToolCall(
            tool_name=tool_name,
            input=input_data,
            output=output_data,
            success=success
        ))
        self.updated_at = datetime.now().timestamp()

    def update_status(self, status: AgentStatus) -> None:
        """Update the agent session status."""
        self.status = status
        self.updated_at = datetime.now().timestamp()

    def update_context(self, key: str, value: Any) -> None:
        """Update the session context with new information."""
        self.context[key] = value
        self.updated_at = datetime.now().timestamp() 