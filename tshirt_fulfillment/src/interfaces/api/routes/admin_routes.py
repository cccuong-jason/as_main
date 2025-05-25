from typing import Any
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from tshirt_fulfillment.src.adapters.services.admin_services import GoogleSheetAdmin
from tshirt_fulfillment.src.interfaces.api.dependencies import get_google_sheet_admin

router = APIRouter(prefix="/admin", tags=["admin"])

# Security - API key authentication
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In production, use a secure method to store and validate API keys
valid_api_keys = ["valid_admin_token", "test_admin_token"]


def get_api_key(api_key: str = Security(api_key_header)):
    """Validate API key for admin endpoints."""
    if api_key not in valid_api_keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
        )
    return api_key


# Admin API Models
class FindSheetRequest(BaseModel):
    criteria: dict[str, Any]


class CreateSheetRequest(BaseModel):
    template_id: str
    data: dict[str, Any]
    sheet_name: str
    share_with: list[str]


class ListFilesRequest(BaseModel):
    folder_id: Optional[str] = None
    file_type: Optional[str] = None


class SummarySheetRequest(BaseModel):
    source_sheet_ids: list[str]
    summary_name: str
    summary_type: str


@router.post("/sheets/find")
async def find_google_sheet(
    request: FindSheetRequest,
    api_key: str = Depends(get_api_key),
    google_sheet_admin: GoogleSheetAdmin = Depends(get_google_sheet_admin),
):
    """Find Google Sheets based on search criteria."""
    result = google_sheet_admin.find_google_sheet(criteria=request.criteria, auth_token=api_key)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/sheets/create")
async def create_google_sheet(
    request: CreateSheetRequest,
    api_key: str = Depends(get_api_key),
    google_sheet_admin: GoogleSheetAdmin = Depends(get_google_sheet_admin),
):
    """Create a new Google Sheet from a template."""
    result = google_sheet_admin.create_google_sheet_from_template(
        template_id=request.template_id,
        data=request.data,
        sheet_name=request.sheet_name,
        share_with=request.share_with,
        auth_token=api_key,
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/drive/list")
async def list_drive_files(
    request: ListFilesRequest,
    api_key: str = Depends(get_api_key),
    google_sheet_admin: GoogleSheetAdmin = Depends(get_google_sheet_admin),
):
    """List files in Google Drive, optionally filtered by folder and type."""
    result = google_sheet_admin.list_drive_files(
        folder_id=request.folder_id, file_type=request.file_type, auth_token=api_key
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/sheets/summary")
async def generate_summary_sheet(
    request: SummarySheetRequest,
    api_key: str = Depends(get_api_key),
    google_sheet_admin: GoogleSheetAdmin = Depends(get_google_sheet_admin),
):
    """Generate a summary sheet from multiple source sheets."""
    result = google_sheet_admin.generate_summary_sheet(
        source_sheet_ids=request.source_sheet_ids,
        summary_name=request.summary_name,
        summary_type=request.summary_type,
        auth_token=api_key,
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
