# Regression tests for Admin functionality
import pytest
from tshirt_fulfillment.core.domain.admin import Admin
from tshirt_fulfillment.core.use_cases.admin_dashboard import AdminDashboard


@pytest.mark.regression
def test_admin_authentication_regression():
    """
    Regression test for admin authentication.
    This test ensures that the bug where admins with invalid credentials
    were being authenticated does not reoccur.
    """
    # Arrange
    admin = Admin(username="admin", password_hash="correct_hash")
    
    # Act/Assert
    with pytest.raises(ValueError, match="Invalid credentials"):
        admin.authenticate(password="wrong_password")


@pytest.mark.regression
def test_admin_order_status_update_regression(mock_order_repository):
    """
    Regression test for order status updates.
    This test ensures that the bug where invalid status transitions
    were being allowed does not reoccur.
    """
    # Arrange
    admin_dashboard = AdminDashboard(order_repository=mock_order_repository)
    
    # Mock an order that is already completed
    mock_order_repository.get_by_id.return_value.status = "completed"
    
    # Act/Assert - Cannot change status from completed to pending
    with pytest.raises(ValueError, match="Invalid status transition"):
        admin_dashboard.update_order_status(order_id="order123", new_status="pending")


@pytest.mark.regression
def test_admin_report_generation_regression(mock_database_with_history):
    """
    Regression test for admin report generation.
    This test ensures that the bug where reports with invalid date ranges
    were being generated does not reoccur.
    """
    # Arrange
    admin_dashboard = AdminDashboard(order_repository=mock_database_with_history)
    
    # Act/Assert - Cannot generate report with end date before start date
    with pytest.raises(ValueError, match="End date must be after start date"):
        admin_dashboard.generate_report(start_date="2023-02-01", end_date="2023-01-01")


@pytest.mark.regression
def test_admin_access_control_regression():
    """
    Regression test for admin access control.
    This test ensures that the bug where unauthorized users
    were gaining admin access does not reoccur.
    """
    # Arrange
    admin = Admin(username="admin", password_hash="correct_hash", role="viewer")
    admin_dashboard = AdminDashboard()
    
    # Act/Assert - Viewer role cannot perform admin actions
    with pytest.raises(PermissionError, match="Insufficient permissions"):
        admin_dashboard.delete_order(admin=admin, order_id="order123")