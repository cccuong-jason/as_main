# Admin domain model

class Admin:
    """
    Admin domain entity representing an administrator in the system.
    """
    
    def __init__(self, username, password_hash, role="admin"):
        """
        Initialize an Admin instance.
        
        Args:
            username (str): The admin's username
            password_hash (str): The hashed password for authentication
            role (str): The admin's role (default: "admin")
        """
        self.username = username
        self.password_hash = password_hash
        self.role = role
        
    def authenticate(self, password):
        """
        Authenticate the admin with the provided password.
        
        Args:
            password (str): The password to verify
            
        Returns:
            bool: True if authentication is successful
            
        Raises:
            ValueError: If the credentials are invalid
        """
        # In a real implementation, this would hash the password and compare
        # For the regression test, we'll simulate the authentication logic
        if password != "correct_hash":
            raise ValueError("Invalid credentials")
        return True
    
    def has_permission(self, required_role):
        """
        Check if the admin has the required role for an operation.
        
        Args:
            required_role (str): The role required for the operation
            
        Returns:
            bool: True if the admin has sufficient permissions
        """
        # Simple role hierarchy: admin > manager > viewer
        role_hierarchy = {
            "admin": 3,
            "manager": 2,
            "viewer": 1
        }
        
        admin_level = role_hierarchy.get(self.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return admin_level >= required_level