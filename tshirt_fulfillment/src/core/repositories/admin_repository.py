from typing import Optional

from tshirt_fulfillment.src.core.domain.admin import AdminUser


class AdminRepository:
    """Repository for managing admin users in the system."""

    def __init__(self, session=None):
        """Initialize the repository with an optional session.

        Args:
            session: Optional database session. If None, uses in-memory
                    storage.
        """
        self._admins = {}  # In-memory storage
        self.session = session

    def save(self, admin: AdminUser) -> AdminUser:
        """Save an admin user to the repository.

        Args:
            admin: The admin user to save

        Returns:
            AdminUser: The saved admin user
        """
        if self.session:
            self.session.add(admin)
            self.session.commit()
        else:
            self._admins[admin.id] = admin
        return admin

    def get_by_id(self, admin_id: str) -> Optional[AdminUser]:
        """Get an admin user by their ID.

        Args:
            admin_id: The ID of the admin to retrieve

        Returns:
            Optional[AdminUser]: The admin if found, None otherwise
        """
        if self.session:
            return self.session.query(AdminUser).filter_by(id=admin_id).first()
        return self._admins.get(admin_id)

    def get_by_email(self, email: str) -> Optional[AdminUser]:
        """Get an admin user by their email.

        Args:
            email: The email of the admin to retrieve

        Returns:
            Optional[AdminUser]: The admin if found, None otherwise
        """
        if self.session:
            return self.session.query(AdminUser).filter_by(email=email).first()
        return next((admin for admin in self._admins.values() if admin.email == email), None)

    def get_all(self) -> list[AdminUser]:
        """Get all admin users in the repository.

        Returns:
            List[AdminUser]: List of all admin users
        """
        if self.session:
            return self.session.query(AdminUser).all()
        return list(self._admins.values())

    def update(self, admin: AdminUser) -> AdminUser:
        """Update an existing admin user.

        Args:
            admin: The admin user to update

        Returns:
            AdminUser: The updated admin user
        """
        if self.session:
            self.session.add(admin)
            self.session.commit()
        else:
            if admin.id not in self._admins:
                raise ValueError("Admin user not found")
            self._admins[admin.id] = admin
        return admin

    def delete(self, admin_id: str) -> bool:
        """Delete an admin user by their ID.

        Args:
            admin_id: The ID of the admin to delete

        Returns:
            bool: True if successful
        """
        if self.session:
            admin = self.session.query(AdminUser).filter_by(id=admin_id).first()
            if not admin:
                raise ValueError("Admin user not found")
            self.session.delete(admin)
            self.session.commit()
        else:
            if admin_id not in self._admins:
                raise ValueError("Admin user not found")
            del self._admins[admin_id]
        return True
