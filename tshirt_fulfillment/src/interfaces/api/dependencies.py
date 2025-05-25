from fastapi import Depends
from sqlalchemy.orm import Session

from tshirt_fulfillment.src.adapters.services.admin_services import GoogleSheetAdmin
from tshirt_fulfillment.src.config.settings import Config
from tshirt_fulfillment.src.core.repositories.order_repository import OrderRepository
from tshirt_fulfillment.src.core.use_cases.order_processor import TShirtFulfillmentAgent


def get_db():
    """Get database session."""
    # TODO: Implement proper database session management
    return None


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    """Get order repository instance."""
    return OrderRepository(session=db)


def get_agent() -> TShirtFulfillmentAgent:
    """Get AI agent instance."""
    return TShirtFulfillmentAgent(redis_url=Config.REDIS_URL, model_name=Config.LLM_PROVIDER)


def get_google_sheet_admin() -> GoogleSheetAdmin:
    """Get Google Sheet admin service instance."""
    return GoogleSheetAdmin()
