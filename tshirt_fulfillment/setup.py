from setuptools import find_packages
from setuptools import setup

setup(
    name="tshirt_fulfillment",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.0.267",
        "redis>=4.5.1",
        "ollama>=0.1.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "langchain-community>=0.0.10",
        "openpyxl>=3.1.0",
        "google-api-python-client>=2.100.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=1.0.0",
        "diffusers>=0.19.0",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.65.0",
        "pytest>=6.0.0",
        "pytest-cov>=2.12.0",
    ],
    python_requires=">=3.8",
)
