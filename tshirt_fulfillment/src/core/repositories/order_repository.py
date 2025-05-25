from typing import Optional

from tshirt_fulfillment.src.core.domain.order import Order


class OrderRepository:
    """Repository for managing orders in the system."""

    def __init__(self, session=None):
        """Initialize the repository with an optional session.

        Args:
            session: Optional database session. If None, uses in-memory storage.
        """
        self._orders = {}  # In-memory storage
        self.session = session

    def save(self, order: Order) -> Order:
        """Save an order to the repository.

        Args:
            order: The order to save

        Returns:
            Order: The saved order
        """
        if self.session:
            self.session.add(order)
            self.session.commit()
        else:
            self._orders[order.id] = order
        return order

    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Get an order by its ID.

        Args:
            order_id: The ID of the order to retrieve

        Returns:
            Optional[Order]: The order if found, None otherwise
        """
        if self.session:
            return self.session.query(Order).filter_by(id=order_id).first()
        return self._orders.get(order_id)

    def get_all(self) -> list[Order]:
        """Get all orders in the repository.

        Returns:
            List[Order]: List of all orders
        """
        if self.session:
            return self.session.query(Order).all()
        return list(self._orders.values())

    def update(self, order: Order) -> Order:
        """Update an existing order.

        Args:
            order: The order to update

        Returns:
            Order: The updated order
        """
        if self.session:
            self.session.add(order)
            self.session.commit()
        else:
            if order.id not in self._orders:
                raise ValueError("Order not found")
            self._orders[order.id] = order
        return order

    def delete(self, order_id: str) -> bool:
        """Delete an order by its ID.

        Args:
            order_id: The ID of the order to delete

        Returns:
            bool: True if successful
        """
        if self.session:
            order = self.session.query(Order).filter_by(id=order_id).first()
            if not order:
                raise ValueError("Order not found")
            self.session.delete(order)
            self.session.commit()
        else:
            if order_id not in self._orders:
                raise ValueError("Order not found")
            del self._orders[order_id]
        return True
