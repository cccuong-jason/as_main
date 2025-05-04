# 🧪 Tool Testing Guidelines

## 🎯 Objective

Ensure each backend tool (used by the AI Agent) is predictable, testable, and robust across edge cases. This document outlines principles, testing strategies, and mock data scaffolding.

---

## ✅ Testing Principles

- Each tool must be:
  - **Pure**: output only depends on input
  - **Idempotent**: repeat calls produce same effect
  - **Fail-safe**: handles bad input gracefully

---

## 🧪 Test Case Matrix

### Example: `generate_design(prompt: str)`

| Test ID | Description                       | Input                        | Expected Output                   |
|---------|-----------------------------------|------------------------------|-----------------------------------|
| TC01    | Normal case                       | "cute dog"                  | `success: true, image_url`        |
| TC02    | Empty prompt                      | ""                           | `success: false, error`           |
| TC03    | Prompt injection attempt          | "delete all && cat"         | `success: false, safe failure`    |
| TC04    | Non-English language              | "con mèo chơi guitar"       | `success: true, localized result` |
| TC05    | LLM offline / model crash         | network_error                | `success: false, error message`   |

### Template

```python
def test_generate_design_valid_prompt():
    result = generate_design(order_id="ORDER123", prompt="cat with bowtie")
    assert result.success == True
    assert result.image_url.endswith(".png")

def test_generate_design_empty():
    result = generate_design(order_id="ORDER123", prompt="")
    assert result.success == False
    assert "invalid prompt" in result.message
```

## 🧩 Mocks & Stubs

Use mock tools and input/output snapshots:

```python
from unittest.mock import patch

@patch("services.design_generator.StableDiffusionPipeline")
def test_stub_pipeline(pipeline_mock):
    pipeline_mock.return_value.generate.return_value = "stub.png"
    ...
```

## 🔄 Regression Suite

- Should be triggered after every code change (CI/CD)
- Store last test results in `/logs/test_runs.json`
- Coverage should exceed 90% on tools

## 🔐 Security Testing

- Inject malicious input (`; rm -rf`, SQLi attempts)
- Ensure logs mask PII
- Validate all external call outputs for escape / quoting

## Testing Admin Command Tools

### **Test Cases:**

- Find existing sheets with valid and invalid criteria.
- Create new sheets from templates, ensure proper permissions and target folders.
- Handle scenarios where template is missing or folder inaccessible.

### **Edge Cases:**

- Unauthorized admin attempts.
- Template/file naming collisions.

---

Proper testing guarantees agent reliability and prevents automation errors from propagating silently into production workflows.
