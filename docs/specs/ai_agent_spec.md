# 🧠 AI Agent Layer Specification (LLM-Powered with Tool Calling)

## 🎯 Purpose

This module defines a **goal-directed AI Agent** that autonomously determines how to handle an order end-to-end, powered by **LLM-based planning and tool calling**. It acts as the intelligent orchestrator between the UI, backend services, and external APIs.

## 🧱 Core Concepts

### Agent Architecture

- **LLM-Powered Planning Engine**: Uses a model (OpenAI, LLaMA, Mistral, etc.) to reason about what to do next based on current state and history.
- **Tool Registry**: All backend services (generate design, create excel, upload to drive, notify customer, etc.) are registered as callable tools that the agent can invoke.
- **Agent Memory**:
  - **Short-term memory**: Current session context (order status, last tool result)
  - **Long-term memory**: Past customer orders, preferences, success/failure history (can be stored in vector DB or Redis)
- **Execution Loop Strategy**: Uses ReAct (Reason + Act), Chain-of-Thought, or Plan-and-Act style prompting with intermediate feedback and corrections.

### Tool Calling Example

Each backend service is exposed as a callable tool with clear schema:

```python
@tool
def generate_design(order_id: str, prompt: str) -> str:
    """Generates a T-shirt design image based on prompt. Returns image path."""
    ...

@tool
def create_excel_file(order_id: str, customer_info: Dict) -> str:
    """Generates an Excel order sheet based on customer info. Returns file path."""
    ...
```

The LLM is given the goal, tool descriptions, current context, and it generates the next action plan dynamically:

```plaintext
Goal: Fulfill Order #1234
Context: Customer has uploaded a sample image, requested a blue shirt with flower logo.
Tools: generate_design, upload_to_drive, create_excel_file, notify_customer
Plan:
1. Use generate_design with prompt "flower logo on blue shirt"
2. Upload design to Drive
3. Create Excel file with order info
4. Notify customer for approval
```

## 🔁 Agent Execution Loop

1. **Start**: Order is received via API/webhook → create AgentSession
2. **Context Builder**: Assemble all available data (customer message, uploaded images, selected options)
3. **Tool Registry Injection**: Dynamically load available tools from registry
4. **LLM Planning**: Generate next action based on goal + context + available tools
5. **Tool Execution**: Call the selected tool with parameters
6. **Result Processing**: Update context with tool result
7. **Loop or Complete**: Either return to step 4 or finish if goal achieved

## 🧠 Agent Roles and Flows

The AI Agent supports two distinct roles and flows:

### 1. Customer Order Flow

- **Purpose**: Process customer T-shirt orders from design to fulfillment
- **Trigger**: New order submission from customer
- **Tools Used**: Design generation, Excel creation, Drive upload, customer notification
- **Flow Pattern**: Sequential with approval gates
- **Example Goal**: "Fulfill order #78910 with custom design of a cat playing guitar on a red shirt."

### 2. Admin Command Flow

- **Purpose**: Execute administrative operations on Google Drive and Sheets
- **Trigger**: Direct command from admin user
- **Tools Used**: Google Sheet search/creation, Drive file listing, summary generation
- **Flow Pattern**: Direct command interpretation and execution
- **Example Goal**: "Find existing Google sheet for client ABC order from last month."
- **Security**: Requires admin authentication and authorization

## 🔄 Agent State Management

### Session State

```typescript
type AgentSession = {
  session_id: string;
  user_type: "customer" | "admin";
  goal: string;
  context: Record<string, any>; // For customer: order details; For admin: command details
  history: ToolCall[];
  status: "active" | "completed" | "failed";
  created_at: Date;
  updated_at: Date;
};

type ToolCall = {
  tool_name: string;
  input: Record<string, any>;
  output: Record<string, any>;
  success: boolean;
  timestamp: Date;
};
```

## 🔍 Agent Prompt Structure

### Customer Flow Prompt

```markdown
You are an AI Agent responsible for handling custom T-shirt orders.
Your job is to plan and execute the necessary steps to fulfill each order using the available tools.

## Goal:
{{goal}}

## User Type:
customer

## Context:
{{order_context}}

## Tool Registry:
{{tool_descriptions}}

## History:
{{agent_session_log}}

## Rules:
- Only use listed tools
- Do not guess missing data
- Ask for confirmation when required
- Stop when goal is achieved or failure occurs

## Respond:
Describe the next action and which tool to use, including inputs.
Explain your reasoning before acting.
```

### Admin Flow Prompt

```markdown
### Role: Admin Command Processor

## Goal:
{{goal}}

## User Type:
admin

## Command:
{{admin_command}}

## Context:
{{admin_context}}

## Tool Registry:
{{admin_tool_descriptions}}

## History:
{{agent_session_log}}

## Task:
1. Clearly interpret the admin command.
2. Extract required action and criteria.
3. Execute appropriate backend tool.
4. Confirm explicitly the action taken.

## Rules:
- Only use listed tools
- Prioritize accuracy over confirmation
- Verify all operations before executing
- Stop when goal is achieved or failure occurs

## Respond:
Describe the next action and which tool to use, including inputs.
Explain your reasoning before acting.
```

## 🔒 Security Considerations

- **Role-Based Access Control**: Admin commands require explicit admin authentication
- **Command Validation**: All admin commands are validated against allowed patterns
- **Audit Logging**: All admin operations are logged with detailed audit trail
- **Rate Limiting**: Admin operations are subject to rate limiting to prevent abuse
- **Data Access Restrictions**: Admin tools can only access authorized resources

## 📊 Metrics & Monitoring

- **Success Rate**: % of goals successfully achieved
- **Completion Time**: Time from start to goal completion
- **Tool Usage**: Frequency and success rate of each tool
- **Error Rate**: % of sessions that fail or require human intervention
- **User Satisfaction**: Feedback score from users

---

This specification defines the AI Agent layer that orchestrates the T-shirt order fulfillment process and admin operations through intelligent planning and tool calling.
