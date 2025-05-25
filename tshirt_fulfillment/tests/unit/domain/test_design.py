# Unit tests for Design domain model
import pytest

from tshirt_fulfillment.src.core.domain.design import Design
from tshirt_fulfillment.src.core.domain.design import DesignProvider


def test_design_creation():
    """Test that a design can be created with valid data"""
    # Arrange
    design_data = {
        "id": "design123",
        "prompt": "A t-shirt with a mountain landscape",
        "image_url": "https://example.com/image.png",
        "status": "completed",
    }

    # Act
    design = Design(**design_data)

    # Assert
    assert design.order_id == design_data["id"]
    assert design.parameters.prompt == design_data["prompt"]
    assert design.image_path == design_data["image_url"]
    assert design.success is False  # Default value


def test_design_validation():
    """Test that design validation works correctly"""
    # Arrange/Act/Assert
    with pytest.raises(ValueError):
        Design(
            id="design123",
            prompt="",  # Empty prompt should fail validation
            image_url="https://example.com/image.png",
            status="completed",
        )

    # Test invalid image URL format
    with pytest.raises(ValueError):
        Design(
            id="design123",
            prompt="A valid prompt",
            image_url="invalid-url-format",  # Invalid URL format should fail validation
            status="completed",
        )


def test_design_result_methods():
    """Test that design result methods work correctly"""
    # Arrange
    design = Design(
        id="design123",
        prompt="A t-shirt with a mountain landscape",
        image_url=None,  # No image yet
    )

    # Act - Set successful result
    image_path = "https://example.com/generated_image.png"
    generation_time = 5.67  # seconds
    design.set_result(image_path, generation_time)

    # Assert
    assert design.image_path == image_path
    assert design.generation_time == generation_time
    assert design.success is True
    assert design.error is None

    # Act - Set error
    error_message = "Failed to generate design"
    design.set_error(error_message)

    # Assert
    assert design.error == error_message
    assert design.success is False


def test_design_create_method():
    """Test the create class method"""
    # Arrange
    order_id = "order123"
    prompt = "A t-shirt with a mountain landscape"
    provider = DesignProvider.STABLE_DIFFUSION
    style = "minimalist"
    size = "512x512"

    # Act
    design = Design.create(order_id, prompt, provider, style, size)

    # Assert
    assert design.order_id == order_id
    assert design.parameters.prompt == prompt
    assert design.parameters.style == style
    assert design.parameters.size == size
    assert design.provider == provider
    assert design.success is False


def test_design_filename_property():
    """Test the filename property"""
    # Arrange
    design = Design(id="design123", prompt="A t-shirt with a mountain landscape")

    # Assert - No image path
    assert design.filename is None

    # Act - Set image path
    design.image_path = "/path/to/image123.png"

    # Assert
    assert design.filename == "image123.png"
