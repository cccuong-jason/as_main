# T-shirt Fulfillment AI Agent - Project Structure

This document outlines the new project structure following clean architecture principles, SOLID, and DRY.

## Project Structure

```
/tshirt_fulfillment/
  /core/                  # Domain layer - business logic and entities
    __init__.py
    /domain/              # Domain models and business rules
      __init__.py
      order.py            # Order entity and value objects
      design.py           # Design entity and value objects
    /use_cases/           # Application use cases/services
      __init__.py
      order_processor.py  # Order processing use cases
      design_generator.py # Design generation use cases
      admin_service.py    # Admin functionality use cases

  /adapters/              # Adapter layer - interfaces to external systems
    __init__.py
    /repositories/        # Data access implementations
      __init__.py
      order_repository.py # Order data access
      design_repository.py # Design data access
    /services/            # External service adapters
      __init__.py
      llm_service.py      # LLM service adapter
      drive_service.py    # Google Drive service adapter
      excel_service.py    # Excel generation service

  /infrastructure/        # Infrastructure layer - frameworks and drivers
    __init__.py
    /persistence/         # Database implementations
      __init__.py
      redis_client.py     # Redis implementation
    /ai/                  # AI implementations
      __init__.py
      ollama_client.py    # Ollama implementation
      stable_diffusion.py # Stable Diffusion implementation
    /external/            # External API implementations
      __init__.py
      google_api.py       # Google API implementation

  /interfaces/            # Interface layer - delivery mechanisms
    __init__.py
    /api/                 # API interfaces
      __init__.py
      fastapi_app.py      # FastAPI application
      routes.py           # API routes
      models.py           # API request/response models
    /cli/                 # Command-line interfaces
      __init__.py
      admin_cli.py        # Admin CLI

  /config/                # Configuration
    __init__.py
    settings.py           # Application settings
    logging_config.py     # Logging configuration

  /utils/                 # Utility functions and helpers
    __init__.py
    logging.py            # Logging utilities
    validators.py         # Validation utilities

  main.py                 # Application entry point
  requirements.txt        # Dependencies
  .env.example            # Example environment variables
  README.md               # Project documentation
  Dockerfile              # Docker configuration
  docker-compose.yml      # Docker Compose configuration
```

## Implementation Plan

1. Create the directory structure
2. Move and refactor the existing code into the new structure
3. Update imports and references
4. Create proper package initialization files
5. Update configuration handling
6. Implement proper dependency injection
7. Add comprehensive documentation

## Benefits of New Structure

- **Separation of Concerns**: Each layer has a specific responsibility
- **Dependency Rule**: Dependencies point inward (core doesn't depend on outer layers)
- **Testability**: Easy to test each component in isolation
- **Maintainability**: Clear organization makes code easier to maintain
- **Scalability**: Easy to add new features without modifying existing code
- **Reusability**: Components can be reused across the application
