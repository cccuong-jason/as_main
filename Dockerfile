# Dockerfile for T-shirt Fulfillment AI Agent

FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY . .

# Create directories for data
RUN mkdir -p tshirt_fulfillment/designs tshirt_fulfillment/orders && \
    chmod -R 777 tshirt_fulfillment/designs tshirt_fulfillment/orders

# Set Python path
ENV PYTHONPATH=/app

# Expose port for API
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["poetry", "run", "uvicorn", "tshirt_fulfillment.src.interfaces.api.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
