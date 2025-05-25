"""Constants used throughout the application."""

from enum import Enum

# API Constants
API_KEY_NAME = "X-API-Key"
VALID_API_KEYS = ["valid_admin_token", "test_admin_token"]


# Order Status Constants
class OrderStatus(str, Enum):
    """Order status enumeration."""

    RECEIVED = "received"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


# Google Sheets Constants
class GoogleSheetConstants:
    """Constants for Google Sheets operations."""

    DEFAULT_SHEET_NAME = "T-Shirt Orders"
    DEFAULT_SUMMARY_NAME = "Order Summary"
    DEFAULT_SUMMARY_TYPE = "daily"


# Redis Constants
class RedisConstants:
    """Constants for Redis operations."""

    DEFAULT_REDIS_URL = "redis://localhost:6379/0"
    ORDER_KEY_PREFIX = "order:"
    SESSION_KEY_PREFIX = "session:"


# Logging Constants
class LoggingConstants:
    """Constants for logging configuration."""

    DEFAULT_LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
