# Configuration loader for T-shirt Fulfillment AI Agent

import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for T-shirt Fulfillment AI Agent."""
    
    # Redis Configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mistral")  # 'mistral', 'llama2', or 'openai'
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Only needed if using OpenAI
    
    # Google Drive API Configuration
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN", "")
    
    # Design Generator Configuration
    DESIGN_GENERATOR = os.getenv("DESIGN_GENERATOR", "local")  # 'local' or 'api'
    DALLE_API_KEY = os.getenv("DALLE_API_KEY", "")  # Only needed if using DALL-E
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    
    # Application Settings
    MAX_AGENT_ITERATIONS = int(os.getenv("MAX_AGENT_ITERATIONS", "10"))
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "vi")
    
    # Paths Configuration
    DESIGN_OUTPUT_DIR = os.getenv("DESIGN_OUTPUT_DIR", "designs")
    ORDER_FILES_DIR = os.getenv("ORDER_FILES_DIR", "orders")
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration based on provider."""
        if cls.LLM_PROVIDER == "openai":
            return {
                "provider": "openai",
                "api_key": cls.OPENAI_API_KEY,
                "model": "gpt-3.5-turbo",  # Use cheaper model by default
                "temperature": 0.7
            }
        else:
            return {
                "provider": "ollama",
                "model": cls.LLM_PROVIDER,  # Use the provider name as the model name for Ollama
                "temperature": 0.7
            }
    
    @classmethod
    def get_design_generator_config(cls) -> Dict[str, Any]:
        """Get design generator configuration."""
        if cls.DESIGN_GENERATOR == "api":
            return {
                "provider": "dalle",
                "api_key": cls.DALLE_API_KEY,
                "size": "1024x1024"
            }
        else:
            return {
                "provider": "stable_diffusion",
                "model": "runwayml/stable-diffusion-v1-5",
                "use_gpu": True  # Set to False if no GPU available
            }
    
    @classmethod
    def get_google_drive_config(cls) -> Optional[Dict[str, str]]:
        """Get Google Drive configuration if available."""
        if cls.GOOGLE_CLIENT_ID and cls.GOOGLE_CLIENT_SECRET and cls.GOOGLE_REFRESH_TOKEN:
            return {
                "client_id": cls.GOOGLE_CLIENT_ID,
                "client_secret": cls.GOOGLE_CLIENT_SECRET,
                "refresh_token": cls.GOOGLE_REFRESH_TOKEN
            }
        return None
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return os.getenv("ENVIRONMENT", "development").lower() == "production"
    
    @classmethod
    def get_admin_tools_config(cls) -> Dict[str, Any]:
        """Get admin tools configuration."""
        # Use the same Google Drive credentials for admin tools
        google_config = cls.get_google_drive_config() or {}
        
        return {
            **google_config,
            "audit_logging": True,
            "log_dir": os.getenv("ADMIN_LOG_DIR", "admin_logs")
        }


# Example usage
if __name__ == "__main__":
    # Print current configuration
    print(f"LLM Provider: {Config.LLM_PROVIDER}")
    print(f"Design Generator: {Config.DESIGN_GENERATOR}")
    print(f"Redis URL: {Config.REDIS_URL}")
    print(f"Default Language: {Config.DEFAULT_LANGUAGE}")
    
    # Get LLM configuration
    llm_config = Config.get_llm_config()
    print(f"\nLLM Config: {llm_config}")
    
    # Get design generator configuration
    design_config = Config.get_design_generator_config()
    print(f"\nDesign Generator Config: {design_config}")