# Script to implement the new project structure
import os
import shutil

# Define the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the new project directory
PROJECT_DIR = os.path.join(BASE_DIR, 'tshirt_fulfillment')

# Define the structure
DIRECTORY_STRUCTURE = [
    # Core layer
    'core',
    'core/domain',
    'core/use_cases',
    
    # Adapters layer
    'adapters',
    'adapters/repositories',
    'adapters/services',
    
    # Infrastructure layer
    'infrastructure',
    'infrastructure/persistence',
    'infrastructure/ai',
    'infrastructure/external',
    
    # Interfaces layer
    'interfaces',
    'interfaces/api',
    'interfaces/cli',
    
    # Configuration
    'config',
    
    # Utilities
    'utils',
]

# Create the directory structure
def create_directory_structure():
    print(f"Creating project structure in {PROJECT_DIR}")
    
    # Create the main project directory if it doesn't exist
    if not os.path.exists(PROJECT_DIR):
        os.makedirs(PROJECT_DIR)
    
    # Create each directory in the structure
    for directory in DIRECTORY_STRUCTURE:
        dir_path = os.path.join(PROJECT_DIR, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            # Create __init__.py file in each directory
            with open(os.path.join(dir_path, '__init__.py'), 'w') as f:
                f.write('# Package initialization\n')
    
    # Create main.py in the project root
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write('# T-shirt Fulfillment AI Agent - Main entry point\n\n'
                'from interfaces.api.fastapi_app import create_app\n\n'
                'app = create_app()\n\n'
                'if __name__ == "__main__":\n'
                '    import uvicorn\n'
                '    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)\n')
    
    # Create README.md in the project root
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('# T-shirt Fulfillment AI Agent\n\n'
                'An AI-powered system for automating T-shirt order fulfillment.\n\n'
                '## Setup Instructions\n\n'
                '1. Install dependencies: `pip install -r requirements.txt`\n'
                '2. Configure environment variables: Copy `.env.example` to `.env` and update values\n'
                '3. Run the application: `python main.py`\n')
    
    print("Directory structure created successfully!")

# Move existing files to the new structure
def move_existing_files():
    # Note: The sample_implementation directory has been removed as part of the migration to clean architecture
    # This function is kept for historical reference but will not perform any operations
    
    # File mappings are no longer needed as sample_implementation directory has been removed
    # This section is kept for historical reference
    file_mappings = {}
    
    # The rest of this function is no longer needed as sample_implementation directory has been removed
    # This function is kept for historical reference only
    pass

    print("Note: No files were moved as sample_implementation directory has been removed.")

# Main execution
if __name__ == "__main__":
    create_directory_structure()
    move_existing_files()
    print("\nProject structure implementation completed!")
    print(f"New project structure is available at: {PROJECT_DIR}")
    print("\nNext steps:")
    print("1. Update imports in the moved files")
    print("2. Refactor code to follow clean architecture principles")
    print("3. Implement proper dependency injection")
    print("4. Add comprehensive documentation")