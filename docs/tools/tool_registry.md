# 🛠️ Tool Registry Specification

## 🎯 Purpose
This document defines the tools available for the AI Agent to use, including their purpose, input/output structure, access constraints, and error handling expectations. Each tool is considered an atomic, testable unit that performs a single well-defined function.

---

## 📦 Tool Format
Every tool should follow this structure:
```python
@tool
def tool_name(arg1: Type, arg2: Type) -> OutputType:
    """Brief description of what the tool does."""
    # Implementation
    return output
```

### Requirements for Each Tool
- **Input type** must be strictly typed (str, int, Dict, etc.)
- **Output** should be structured (e.g., dict with status, message, data)
- Must fail gracefully with custom error handling
- Docstring should include:
  - Clear function description
  - When to use
  - Input/output schema explanation (use JSONSchema if needed)

---

## 📚 Registered Tools

### Customer Flow Tools

#### 1. `generate_design`
- **Description**: Creates a design image based on a text prompt (via Stable Diffusion)
- **Input**: `order_id (str)`, `prompt (str)`
- **Output**: `{ success: bool, image_url: str, error?: str }`
- **Failure Modes**: LLM hallucinating wrong concept, GPU timeout, blank image
- **Retries**: 2 with backoff

#### 2. `create_excel_file`
- **Description**: Generates a .xlsx order sheet based on provided customer/order metadata
- **Input**: `order_id (str)`, `customer_info (Dict)`
- **Output**: `{ success: bool, file_path: str }`
- **Failure Modes**: Wrong template path, missing fields

#### 3. `upload_to_drive`
- **Description**: Uploads a file to the designated Google Drive folder
- **Input**: `order_id (str)`, `file_path (str)`, `file_type ("design" | "excel")`
- **Output**: `{ success: bool, file_url: str }`
- **Precondition**: Folder must already exist (created in prior step)

#### 4. `notify_customer`
- **Description**: Sends email notification to customer with order status
- **Input**: `order_id (str)`, `message (str)`, `include_images (bool)`
- **Output**: `{ success: bool, message_id?: str }`
- **Failure Modes**: Email service down, invalid email address

### Admin Flow Tools

#### 5. `find_google_sheet`
- **Description**: Searches Google Drive for sheets matching specified criteria
- **Input**: `criteria (Dict)` with optional fields: `client_name`, `time_period`, `sheet_name`, `folder_path`
- **Output**: `{ success: bool, sheets: List[Dict], error?: str }`
- **Failure Modes**: No matching sheets, Google API rate limit, authentication failure
- **Security**: Requires admin authentication

#### 6. `create_google_sheet_from_template`
- **Description**: Creates a new Google Sheet based on a template and populates it with data
- **Input**: `template_id (str)`, `data (Dict)`, `sheet_name (str)`, `share_with (List[str])`
- **Output**: `{ success: bool, sheet_url: str, error?: str }`
- **Failure Modes**: Template not found, insufficient permissions, invalid data format
- **Security**: Requires admin authentication

#### 7. `list_drive_files`
- **Description**: Lists files in a specified Google Drive folder with optional filtering
- **Input**: `folder_path (str)`, `filter (Dict)` with optional fields: `file_type`, `created_after`, `created_before`, `name_contains`
- **Output**: `{ success: bool, files: List[Dict], error?: str }`
- **Failure Modes**: Folder not found, insufficient permissions
- **Security**: Requires admin authentication

#### 8. `generate_summary_sheet`
- **Description**: Creates a summary Google Sheet based on multiple data sources
- **Input**: `data_sources (List[str])`, `summary_type ("daily" | "weekly" | "monthly")`, `output_name (str)`
- **Output**: `{ success: bool, sheet_url: str, error?: str }`
- **Failure Modes**: Data sources not accessible, calculation errors
- **Security**: Requires admin authentication

---

## 🔒 Security Considerations

### Authentication & Authorization
- All tools must verify the caller has appropriate permissions
- Admin-only tools require explicit admin role verification
- Rate limiting applies to prevent abuse

### Data Validation
- All inputs must be sanitized and validated
- File paths must be normalized and checked for directory traversal
- User-provided content must be scanned for malicious content

### Error Handling
- Never expose internal errors to users
- Log detailed errors for debugging
- Return user-friendly error messages

---

## 📊 Monitoring & Logging

- Each tool call is logged with:
  - Timestamp
  - Tool name
  - Input parameters (sanitized)
  - Output status
  - Execution time
  - User/session ID

- Performance metrics tracked:
  - Success rate
  - Average execution time
  - Error frequency by type

---

This registry is the canonical source of truth for all tools available to the AI Agent.
