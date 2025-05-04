# Script to update imports in the moved files
import os
import re

# Define the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'tshirt_fulfillment')

# Define import mappings (old import -> new import)
IMPORT_MAPPINGS = {
    'from agent import': 'from tshirt_fulfillment.core.use_cases.order_processor import',
    'from config import': 'from tshirt_fulfillment.config.settings import',
    'from admin_tools import': 'from tshirt_fulfillment.adapters.services.admin_services import',
    'from tools import': 'from tshirt_fulfillment.adapters.services.external_services import',
}

# Files to update
FILES_TO_UPDATE = [
    os.path.join(PROJECT_DIR, 'interfaces', 'api', 'fastapi_app.py'),
    os.path.join(PROJECT_DIR, 'core', 'use_cases', 'order_processor.py'),
    os.path.join(PROJECT_DIR, 'adapters', 'services', 'admin_services.py'),
    os.path.join(PROJECT_DIR, 'adapters', 'services', 'external_services.py'),
]

# Function to update imports in a file
def update_imports(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Apply import mappings
    updated_content = content
    for old_import, new_import in IMPORT_MAPPINGS.items():
        updated_content = updated_content.replace(old_import, new_import)
    
    # Write updated content back to file
    if updated_content != content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Updated imports in {file_path}")
        return True
    else:
        print(f"No imports to update in {file_path}")
        return False

# Update imports in all files
def update_all_imports():
    updated_files = 0
    for file_path in FILES_TO_UPDATE:
        if update_imports(file_path):
            updated_files += 1
    
    print(f"\nUpdated imports in {updated_files} files")

# Create a README file with instructions
def create_readme():
    readme_path = os.path.join(BASE_DIR, 'tshirt_fulfillment', 'README.md')
    with open(readme_path, 'w') as f:
        f.write('''
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
''')
    print(f"Created README at {readme_path}")

# Main execution
if __name__ == "__main__":
    update_all_imports()
    create_readme()
    print("\nImport updates completed!")
    print("\nNext steps:")
    print("1. Further refactor code to follow clean architecture principles")
    print("2. Implement proper dependency injection")
    print("3. Add comprehensive documentation")
    print("4. Create unit tests for each component")