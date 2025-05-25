from dataclasses import dataclass
from typing import Optional

from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from core.domain.agent import AgentRole
from core.domain.agent import AgentSession
from core.domain.agent import AgentStatus
from core.domain.tools import ToolRegistry
from core.use_cases.design_generator import DesignGenerator
from core.use_cases.order_processor import OrderProcessor


@dataclass
class AgentServiceResult:
    """Result of agent service operations"""

    success: bool
    session: Optional[AgentSession] = None
    error: Optional[str] = None


class AgentService:
    """Service for managing AI agent sessions and execution.

    This service integrates with LangChain to provide intelligent
    order processing and admin operations.
    """

    def __init__(
        self,
        order_processor: OrderProcessor,
        design_generator: DesignGenerator,
        tool_registry: ToolRegistry,
        redis_url: str = "redis://localhost:6379/0",
    ):
        """Initialize the agent service.

        Args:
            order_processor: Service for processing orders
            design_generator: Service for generating designs
            tool_registry: Registry of available tools
            redis_url: URL for Redis connection
        """
        self.order_processor = order_processor
        self.design_generator = design_generator
        self.tool_registry = tool_registry
        self.redis_url = redis_url

        # Initialize LLM
        self.llm = Ollama(model="mistral")

    def _create_agent_session(
        self, session: AgentSession, tools: list, system_prompt: str
    ) -> AgentServiceResult:
        """Create an agent session with the given tools and prompt.

        Args:
            session: The session to configure
            tools: List of tools to use
            system_prompt: System prompt for the agent

        Returns:
            AgentServiceResult with success status and session
        """
        try:
            # Initialize memory
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            # Get tool names and handlers
            tool_names = [str(tool.name) for tool in tools]
            tool_handlers = list(tools)

            # Create agent with string tool names
            prompt = PromptTemplate(
                input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
                template=(
                    f"{system_prompt}\n"
                    "Available tools: {tools}\n"
                    "Tool names: {tool_names}\n"
                    "{input}\n"
                    "{agent_scratchpad}"
                ),
            )

            # Create agent with handlers but pass string names to prompt
            agent = create_react_agent(llm=self.llm, tools=tool_handlers, prompt=prompt)

            # Create executor with handlers
            executor = AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=tool_handlers,
                memory=memory,
                verbose=True,
                handle_parsing_errors=True,
            )

            # Store executor and string tool names in session
            session.update_context("executor", executor)
            session.update_context("tool_names", tool_names)
            session.update_context("tools", tools)

            return AgentServiceResult(success=True, session=session)
        except Exception as e:
            return AgentServiceResult(success=False, error=str(e))

    def create_customer_session(self, order_id: str) -> AgentServiceResult:
        """Create a new customer session for order processing.

        Args:
            order_id: ID of the order to process

        Returns:
            AgentServiceResult with success status and session
        """
        try:
            # Validate order exists first
            order_result = self.order_processor.get_order(order_id)
            if not order_result.success:
                return AgentServiceResult(success=False, error=f"Order not found: {order_id}")

            # Create session
            session = AgentSession.create_customer_session(order_id)

            # Get available tools
            tools = self.tool_registry.get_customer_tools()

            # Create agent session
            return self._create_agent_session(
                session=session,
                tools=tools,
                system_prompt="You are an AI agent for t-shirt order processing.",
            )
        except Exception as e:
            return AgentServiceResult(success=False, error=str(e))

    def create_admin_session(self, command_id: str) -> AgentServiceResult:
        """Create a new admin session for command processing.

        Args:
            command_id: ID of the command to process

        Returns:
            AgentServiceResult with success status and session
        """
        try:
            # Create session
            session = AgentSession.create_admin_session(command_id)

            # Get available tools
            tools = self.tool_registry.get_admin_tools()

            # Create agent session
            return self._create_agent_session(
                session=session, tools=tools, system_prompt="You are an AI admin agent."
            )
        except Exception as e:
            return AgentServiceResult(success=False, error=str(e))

    def execute_session(self, session: AgentSession) -> AgentServiceResult:
        """Execute an agent session.

        Args:
            session: Session to execute

        Returns:
            AgentServiceResult with success status and updated session
        """
        try:
            # Update session status
            session.update_status(AgentStatus.PROCESSING)

            # Get executor from context
            executor = session.context.get("executor")
            if not executor:
                raise ValueError("No executor found in session context")

            # Prepare input based on session role
            if session.role == AgentRole.CUSTOMER:
                # Get order
                order_result = self.order_processor.get_order(session.order_id)
                if not order_result.success:
                    raise ValueError(f"Order not found: {session.order_id}")
                # Execute agent
                result = executor.invoke(
                    {
                        "input": (
                            f"Process order {session.order_id}: "
                            f"{order_result.order.customer_message}"
                        )
                    }
                )
            else:
                # Execute admin command
                result = executor.invoke(
                    {"input": (f"Execute admin command " f"{session.command_id}")}
                )
            # Update session with result
            session.update_context("result", result)
            session.update_status(AgentStatus.COMPLETED)

            return AgentServiceResult(success=True, session=session)
        except Exception as e:
            session.update_status(AgentStatus.FAILED)
            session.update_context("error", str(e))

            return AgentServiceResult(success=False, session=session, error=str(e))
