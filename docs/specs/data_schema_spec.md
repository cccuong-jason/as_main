# 🗂️ Data Schema Specification

## 🎯 Purpose

This document defines the canonical data schemas used throughout the AI Agent system—ensuring consistent structure, validation, and typing across services, memory, and tool interfaces.

---

## 📦 Core Data Types

### 1. `Order` (Primary Entity)

```json
{
  "order_id": "string",            // Unique UUID or slug
  "customer_name": "string",
  "shirt_color": "string",
  "size": "string",                // e.g. "S", "M", "L"
  "design_idea": "string",
  "uploaded_image": "string|null", // Image URL or null
  "language": "string",            // e.g. "en", "vi"
  "status": "enum",               // See `OrderStatus`
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 2. `OrderStatus` (Enum)

```ts
type OrderStatus =
  | "new"
  | "pending_design"
  | "design_ready"
  | "awaiting_approval"
  | "approved"
  | "excel_ready"
  | "completed"
  | "error";
```

### 3. `AdminCommand` (Admin Flow Entity)

```json
{
  "command_id": "string",          // Unique UUID
  "admin_id": "string",           // ID of admin user
  "command_text": "string",       // Natural language command
  "parsed_intent": "enum",        // See `AdminCommandIntent`
  "parsed_parameters": "object",  // Extracted parameters
  "status": "enum",              // See `AdminCommandStatus`
  "result": "object|null",       // Command execution result
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 4. `AdminCommandIntent` (Enum)

```ts
type AdminCommandIntent =
  | "find_sheet"
  | "create_sheet"
  | "list_files"
  | "generate_summary"
  | "unknown";
```

### 5. `AdminCommandStatus` (Enum)

```ts
type AdminCommandStatus =
  | "received"
  | "processing"
  | "completed"
  | "failed";
```

### 6. `ToolResult`

```json
{
  "success": true,
  "message": "string",
  "data": "any" // Depending on tool: image_url, file_path, etc.
}
```

---

## 🧠 Memory Snapshots (Per Agent Session)

### 1. `CustomerSessionMemory`

```json
{
  "session_id": "string",
  "user_type": "customer",
  "order_id": "string",
  "current_state": "object",      // Current order state
  "tool_history": [                // Array of tool calls
    {
      "tool": "string",
      "input": "object",
      "output": "object",
      "timestamp": "datetime"
    }
  ],
  "last_user_message": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 2. `AdminSessionMemory`

```json
{
  "session_id": "string",
  "user_type": "admin",
  "command_id": "string",
  "current_state": "object",      // Current command state
  "tool_history": [                // Array of tool calls
    {
      "tool": "string",
      "input": "object",
      "output": "object",
      "timestamp": "datetime"
    }
  ],
  "command_text": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

## 📊 Tool Input/Output Schemas

### Customer Flow Tools

#### 1. `generate_design`

- **Input**:

  ```json
  {
    "order_id": "string",
    "prompt": "string"
  }
  ```

- **Output**:

  ```json
  {
    "success": "boolean",
    "image_url": "string",
    "error": "string|null"
  }
  ```

#### 2. `create_excel_file`

- **Input**:

  ```json
  {
    "order_id": "string",
    "customer_info": "object"
  }
  ```

- **Output**:

  ```json
  {
    "success": "boolean",
    "file_path": "string",
    "error": "string|null"
  }
  ```

### Admin Flow Tools

#### 1. `find_google_sheet`

- **Input**:

  ```json
  {
    "criteria": {
      "client_name": "string|null",
      "time_period": "string|null",
      "sheet_name": "string|null",
      "folder_path": "string|null"
    }
  }
  ```

- **Output**:

  ```json
  {
    "success": "boolean",
    "sheets": [
      {
        "name": "string",
        "url": "string",
        "created_at": "datetime",
        "last_modified": "datetime"
      }
    ],
    "error": "string|null"
  }
  ```

#### 2. `create_google_sheet_from_template`

- **Input**:

  ```json
  {
    "template_id": "string",
    "data": "object",
    "sheet_name": "string",
    "share_with": ["string"]
  }
  ```

- **Output**:

  ```json
  {
    "success": "boolean",
    "sheet_url": "string",
    "error": "string|null"
  }
  ```

---

## 🔄 API Request/Response Schemas

### Customer Flow API

#### `POST /orders`

- **Request**:

  ```json
  {
    "customer_name": "string",
    "shirt_color": "string",
    "size": "string",
    "design_idea": "string",
    "uploaded_image": "string|null",
    "language": "string"
  }
  ```

- **Response**:

  ```json
  {
    "order_id": "string",
    "status": "string",
    "message": "string"
  }
  ```

### Admin Flow API

#### `POST /admin/commands`

- **Request**:

  ```json
  {
    "command_text": "string"
  }
  ```

- **Response**:

  ```json
  {
    "command_id": "string",
    "status": "string",
    "message": "string",
    "result": "object|null"
  }
  ```

---

This schema specification ensures consistent data structures across all components of the AI Agent system, supporting both customer order processing and admin command execution flows.
