# Regression tests for Order functionality
import pytest

from tshirt_fulfillment.src.core.domain.order import Order


@pytest.mark.regression
def test_order_quantity_validation_regression():
    """
    Regression test for order quantity validation.
    This test ensures that the bug where orders with quantity=0 were being accepted
    does not reoccur.
    """
    # Arrange/Act/Assert
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        Order(
            id="order123",
            customer_name="Test Customer",
            customer_email="test@example.com",
            design_prompt="A t-shirt with a mountain landscape",
            size="L",
            color="Blue",
            quantity=0,  # Invalid quantity
            status="pending",
        )


@pytest.mark.regression
def test_order_email_validation_regression():
    """
    Regression test for email validation.
    This test ensures that the bug where orders with invalid email formats
    were being accepted does not reoccur.
    """
    # Arrange/Act/Assert
    with pytest.raises(ValueError, match="Invalid email format"):
        Order(
            id="order123",
            customer_name="Test Customer",
            customer_email="invalid-email",  # Invalid email format
            design_prompt="A t-shirt with a mountain landscape",
            size="L",
            color="Blue",
            quantity=1,
            status="pending",
        )


@pytest.mark.regression
def test_duplicate_order_id_regression(mock_order_repository):
    """
    Regression test for duplicate order IDs.
    This test ensures that the bug where orders with duplicate IDs
    were being accepted does not reoccur.
    """
    # Arrange
    # Manually add an order to the repository's dictionary
    mock_order_repository.orders["duplicate_id"] = "dummy_order"

    # Create an order with the same ID
    order = Order(
        id="duplicate_id",
        customer_name="Test Customer",
        customer_email="test@example.com",
        design_prompt="A t-shirt with a mountain landscape",
        size="L",
        color="Blue",
        quantity=1,
        status="pending",
    )

    # Act/Assert - Attempt to save the order with a duplicate ID
    with pytest.raises(ValueError, match="Order with this ID already exists"):
        mock_order_repository.save(order)
