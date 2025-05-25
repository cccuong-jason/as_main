# AI Agent Implementation Plan

## Overview

This document outlines the implementation plan for a cost-effective AI agent system for T-shirt fulfillment, based on the specifications in `ai_agent_spec.md` and the user's requirements for a budget-friendly solution.

## Technology Stack Selection

### LLM Selection (Cost-Optimized)

| Model | Deployment | Pros | Cons | Cost |
|-------|------------|------|------|------|
| **Mistral 7B** | Local via Ollama | Free, No API costs, Privacy | Higher hardware requirements, Less capable than GPT-4 | $0 |
| **Llama 2 (7B/13B)** | Local via Ollama | Free, No API costs, Good reasoning | Higher hardware requirements | $0 |
| **GPT-3.5-Turbo** | OpenAI API | Better reasoning, No local setup | API costs (~$0.002/1K tokens) | Low |
| **GPT-4o-mini** | OpenAI API | Strong reasoning, Better tool use | Higher API costs | Medium |

**Recommendation:** Start with Mistral 7B or Llama 2 locally via Ollama for development and testing. This provides a completely free solution for initial development. If reasoning capabilities are insufficient, consider a hybrid approach where most operations use the local model, but complex reasoning tasks use GPT-3.5-Turbo (minimizing token usage).

### Agent Framework

| Framework | Pros | Cons | Recommendation |
|-----------|------|------|----------------|
| **LangChain** | Mature tool integration, Active community, Vietnamese support | More complex | ✅ Primary choice per user preference |
| **CrewAI** | Simpler for multi-agent systems | Less mature | Alternative if multi-agent becomes priority |
| **Semantic Kernel** | Good Microsoft integration | Less community support | Not recommended |

**Recommendation:** Implement with LangChain as requested, using its tool calling capabilities and memory management features.

### Memory Layer

| Option | Pros | Cons | Cost |
|--------|------|------|------|
| **Redis** | Fast, Simple, Supports TTL | Limited query capabilities | Low (Free for local) |
| **ChromaDB** | Vector search, Better semantic recall | More complex setup | Free (self-hosted) |

**Recommendation:** Use Redis as specified by user preference. It's lightweight, fast, and sufficient for the described use case of 100 concurrent users and 1000 orders/day.

### Design Generation

| Option | Deployment | Pros | Cons | Cost |
|--------|------------|------|------|------|
| **Stable Diffusion** | Local | One-time setup, No API costs | Higher hardware requirements, Slower generation | Free (after setup) |
| **DALL-E API** | OpenAI API | Better quality, Faster | Pay per image (~$0.02-0.04/image) | ~$20-40/1000 images |
| **Midjourney** | API | High quality | Higher cost | Higher |

**Recommendation:** Start with local Stable Diffusion for the most cost-effective approach. If quality is insufficient, consider a hybrid approach where simple designs use local generation and complex designs use DALL-E API (with caching to reduce costs).

## Implementation Phases

### Phase 1: Core Infrastructure Setup

1. **Environment Setup**
   - Local development environment with Python 3.9+
   - Redis installation for memory layer
   - Ollama setup with Mistral 7B or Llama 2

2. **Basic Agent Framework**
   - LangChain installation and configuration
   - Tool registry setup with basic tools
   - Agent execution loop implementation

3. **Memory Management**
   - Redis connection setup
   - Short-term memory implementation
   - Session state management

### Phase 2: Tool Implementation

1. **Design Generation Tool**

   ```python
   @tool
   def generate_design(order_id: str, prompt: str, style: Optional[str] = None) -> Dict[str, Any]:
       """Generates a T-shirt design image based on prompt. Returns image path and metadata."""
       # Implementation using local Stable Diffusion
       try:
           # Generate design using local model
           return {
               "success": True,
               "image_path": f"designs/{order_id}/design.png",
               "prompt_used": prompt,
               "generation_time": "2.3s"
           }
       except Exception as e:
           return {"success": False, "error": str(e)}
   ```

2. **Excel Generation Tool**

   ```python
   @tool
   def create_excel_file(order_id: str, customer_info: Dict[str, Any]) -> Dict[str, Any]:
       """Generates an Excel order sheet based on customer info. Returns file path."""
       try:
           # Implementation using openpyxl
           return {
               "success": True,
               "file_path": f"orders/{order_id}/order_details.xlsx"
           }
       except Exception as e:
           return {"success": False, "error": str(e)}
   ```

3. **Google Drive Integration Tool**

   ```python
   @tool
   def upload_to_drive(order_id: str, file_path: str) -> Dict[str, Any]:
       """Uploads a file to Google Drive and returns the sharing link."""
       try:
           # Implementation using Google Drive API
           return {
               "success": True,
               "drive_url": f"https://drive.google.com/file/d/{order_id}/view"
           }
       except Exception as e:
           return {"success": False, "error": str(e)}
   ```

4. **Customer Notification Tool**

   ```python
   @tool
   def notify_customer(order_id: str, message: str, language: str = "vi") -> Dict[str, Any]:
       """Sends notification to customer about order status."""
       try:
           # Implementation using email or messaging service
           return {
               "success": True,
               "notification_id": f"notif_{order_id}_{int(time.time())}"
           }
       except Exception as e:
           return {"success": False, "error": str(e)}
   ```

### Phase 3: Agent Execution Loop

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import RedisMemory
from langchain.llms import Ollama

# Initialize LLM
llm = Ollama(model="mistral")

# Initialize memory
redis_memory = RedisMemory(redis_url="redis://localhost:6379/0", session_id="{order_id}")

# Create agent with tools
agent = create_react_agent(llm=llm, tools=[generate_design, create_excel_file, upload_to_drive, notify_customer])

# Create agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[generate_design, create_excel_file, upload_to_drive, notify_customer],
    memory=redis_memory,
    verbose=True,
    max_iterations=10  # Prevent infinite loops
)

# Execute agent
def execute_agent_for_order(order_id: str, customer_message: str):
    # Build initial context
    context = {
        "order_id": order_id,
        "customer_message": customer_message,
        "language": "vi"  # Default to Vietnamese
    }

    # Execute agent
    try:
        result = agent_executor.run(input=context)
        # Log critical decision phases
        log_decision_phase(order_id, "execution_complete", result)
        return {"success": True, "result": result}
    except Exception as e:
        log_decision_phase(order_id, "execution_failed", str(e))
        return {"success": False, "error": str(e)}
```

### Phase 4: Error Handling and Logging

```python
def log_decision_phase(order_id: str, phase: str, details: Any):
    """Log critical decision phases for the agent."""
    # Only log critical phases as requested by user
    critical_phases = [
        "order_received",
        "design_generated",
        "excel_created",
        "files_uploaded",
        "customer_notified",
        "approval_received",
        "execution_complete",
        "execution_failed"
    ]

    if phase in critical_phases:
        # Log to database or file
        print(f"[{order_id}] Phase: {phase} - {details}")
        # In production, replace with proper logging
```

## Deployment Strategy

### Local Development (Initial Phase)

1. Setup development environment with all required dependencies
2. Run Redis locally
3. Deploy Ollama with selected LLM
4. Implement and test agent functionality
5. Benchmark performance and cost

### VPS Deployment (Production Phase)

1. Provision VPS with sufficient resources (4+ CPU cores, 8GB+ RAM for LLM)
2. Setup Docker containers for:
   - Redis
   - Ollama with selected LLM
   - Application server
3. Configure proper networking and security
4. Implement monitoring and logging
5. Setup backup strategy for Redis data

## Cost Analysis

### Local Development Costs

- **LLM**: $0 (Ollama with open-source models)
- **Memory**: $0 (Local Redis)
- **Design Generation**: $0 (Local Stable Diffusion)
- **Total**: $0 (excluding development time and hardware)

### Production Costs (VPS)

- **VPS**: ~$20-40/month (4 CPU, 8GB RAM)
- **LLM**: $0 (Ollama with open-source models)
- **Memory**: $0 (Redis on VPS)
- **Design Generation**: $0 (Stable Diffusion on VPS)
- **Total**: ~$20-40/month

### Optional API Costs (If Local Performance Insufficient)

- **OpenAI API** (GPT-3.5-Turbo): ~$2-5/1000 orders (limited usage)
- **DALL-E API**: ~$20-40/1000 designs

## Next Steps

1. **Immediate Actions**
   - Set up local development environment
   - Install Redis and Ollama
   - Implement basic LangChain agent structure

2. **Testing Strategy**
   - Test with sample Vietnamese customer messages
   - Benchmark design generation quality and speed
   - Measure memory usage and performance

3. **Optimization Opportunities**
   - Implement caching for similar design requests
   - Optimize prompts for local LLMs
   - Consider hybrid approach for complex reasoning tasks

## Conclusion

This implementation plan provides a cost-effective approach to building an AI agent for T-shirt fulfillment using LangChain, Redis, and local open-source LLMs. The system is designed to handle the specified load of 100 concurrent users and 1000 orders/day while minimizing costs. The phased approach allows for testing and optimization before moving to production on a VPS.
