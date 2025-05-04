
# T-shirt Fulfillment AI Agent

An AI-powered system for automating T-shirt order fulfillment.

## Project Structure

This project follows clean architecture principles with the following layers:

- **Core**: Domain entities and business logic
- **Adapters**: Interfaces to external systems
- **Infrastructure**: Technical implementations
- **Interfaces**: User interfaces (API, CLI)

## Setup Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your configuration

3. Run the application:
   ```
   python main.py
   ```

## Development

### Project Organization

- **Domain Layer**: Contains business entities and rules
- **Use Case Layer**: Contains application-specific business rules
- **Interface Adapters**: Contains adapters between use cases and external frameworks
- **Frameworks & Drivers**: Contains frameworks and tools like databases, web frameworks, etc.

### Adding New Features

1. Define domain entities in `core/domain/`
2. Implement use cases in `core/use_cases/`
3. Create adapters in `adapters/`
4. Implement infrastructure in `infrastructure/`
5. Expose interfaces in `interfaces/`
