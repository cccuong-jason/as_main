from typing import Optional

from core.domain.design import Design


class DesignRepository:
    """Repository for managing designs in the system."""

    def __init__(self, session=None):
        """Initialize the repository with an optional session.

        Args:
            session: Optional database session. If None, uses in-memory
                    storage.
        """
        self._designs = {}  # In-memory storage
        self.session = session

    def save(self, design: Design) -> Design:
        """Save a design to the repository.

        Args:
            design: The design to save

        Returns:
            Design: The saved design
        """
        if self.session:
            self.session.add(design)
            self.session.commit()
        else:
            self._designs[design.id] = design
        return design

    def get_by_id(self, design_id: str) -> Optional[Design]:
        """Get a design by its ID.

        Args:
            design_id: The ID of the design to retrieve

        Returns:
            Optional[Design]: The design if found, None otherwise
        """
        if self.session:
            return self.session.query(Design).filter_by(id=design_id).first()
        return self._designs.get(design_id)

    def get_all(self) -> list[Design]:
        """Get all designs in the repository.

        Returns:
            List[Design]: List of all designs
        """
        if self.session:
            return self.session.query(Design).all()
        return list(self._designs.values())

    def update(self, design: Design) -> Design:
        """Update an existing design.

        Args:
            design: The design to update

        Returns:
            Design: The updated design
        """
        if self.session:
            self.session.add(design)
            self.session.commit()
        else:
            if design.id not in self._designs:
                raise ValueError("Design not found")
            self._designs[design.id] = design
        return design

    def delete(self, design_id: str) -> bool:
        """Delete a design by its ID.

        Args:
            design_id: The ID of the design to delete

        Returns:
            bool: True if successful
        """
        if self.session:
            design = self.session.query(Design).filter_by(id=design_id).first()
            if not design:
                raise ValueError("Design not found")
            self.session.delete(design)
            self.session.commit()
        else:
            if design_id not in self._designs:
                raise ValueError("Design not found")
            del self._designs[design_id]
        return True
