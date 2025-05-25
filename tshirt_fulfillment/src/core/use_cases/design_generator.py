# Design generation use case

from dataclasses import dataclass
from typing import Optional

from core.domain.design import Design


@dataclass
class DesignGenerationResult:
    """Result of design generation operations"""

    success: bool
    design: Optional[Design] = None
    image_path: Optional[str] = None
    error: Optional[str] = None


class DesignGenerator:
    """Use case for generating T-shirt designs.

    This class implements the business logic for generating designs,
    independent of the specific design generation technology used.
    """

    def __init__(self, design_repository, llm_service=None):
        """Initialize the design generator use case.

        Args:
            design_repository: Repository for design persistence
            llm_service: Service for generating designs using LLM
        """
        self.design_repository = design_repository
        self.llm_service = llm_service

    def generate_design(
        self, order_id: str, prompt: str, style: Optional[str] = None
    ) -> DesignGenerationResult:
        """Generate a T-shirt design based on prompt.

        Args:
            order_id: Unique identifier for the order
            prompt: Design description
            style: Optional style parameter

        Returns:
            DesignGenerationResult with success status, design and image path
        """
        try:
            # Generate image using LLM service if available
            image_url = None
            if self.llm_service:
                image_url = self.llm_service.generate_image(prompt)
            else:
                # Mock image URL for testing
                image_url = f"https://example.com/generated_image_{order_id}.png"

            # Create design entity
            design = Design(
                id=f"design-{order_id}", prompt=prompt, image_url=image_url, status="completed"
            )

            # Save to repository
            saved_design = self.design_repository.save(design)

            return DesignGenerationResult(success=True, design=saved_design, image_path=image_url)
        except Exception as e:
            return DesignGenerationResult(success=False, error=str(e))

    def get_design(self, design_id: str) -> DesignGenerationResult:
        """Get a design by ID.

        Args:
            design_id: ID of the design to retrieve

        Returns:
            DesignGenerationResult with success status and design
        """
        try:
            design = self.design_repository.get_by_id(design_id)
            if not design:
                return DesignGenerationResult(
                    success=False, error=f"Design with ID {design_id} not found"
                )

            return DesignGenerationResult(success=True, design=design, image_path=design.image_path)
        except Exception as e:
            return DesignGenerationResult(success=False, error=str(e))
