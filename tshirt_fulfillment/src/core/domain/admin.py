"""Admin user domain model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AdminUser:
    """Admin user entity.

    Attributes:
        id: Unique identifier for the admin
        email: Admin's email address
        name: Admin's full name
        is_active: Whether the admin account is active
        created_at: Timestamp when the admin was created
        last_login: Timestamp of the admin's last login
        role: Admin's role in the system
    """

    id: str
    email: str
    name: str
    is_active: bool = True
    created_at: datetime = datetime.now()
    last_login: Optional[datetime] = None
    role: str = "admin"

    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.now()

    def deactivate(self) -> None:
        """Deactivate the admin account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the admin account."""
        self.is_active = True
