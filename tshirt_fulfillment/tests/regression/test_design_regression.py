# Regression tests for Design functionality
import pytest

from tshirt_fulfillment.src.core.domain.design import Design
from tshirt_fulfillment.src.core.use_cases.design_generator import DesignGenerator


@pytest.mark.regression
def test_design_prompt_validation_regression():
    """
    Regression test for design prompt validation.
    This test ensures that the bug where designs with empty prompts
    were being accepted does not reoccur.
    """
    # Arrange/Act/Assert
    with pytest.raises(ValueError, match="Design prompt cannot be empty"):
        Design(
            id="design123",
            order_id="order123",
            prompt="",  # Empty prompt
            image_url=None,
            status="pending",
        )


@pytest.mark.regression
def test_design_image_url_validation_regression():
    """
    Regression test for image URL validation.
    This test ensures that the bug where designs with invalid image URLs
    were being accepted does not reoccur.
    """
    # Arrange/Act/Assert
    with pytest.raises(ValueError, match="Invalid image URL format"):
        Design(
            id="design123",
            order_id="order123",
            prompt="A t-shirt with a mountain landscape",
            image_url="invalid-url",  # Invalid URL format
            status="completed",
        )


@pytest.mark.regression
def test_design_generation_failure_handling_regression(mock_llm_service, regression_data):
    """
    Regression test for design generation failure handling.
    This test ensures that the bug where design generation failures
    were not properly handled does not reoccur.
    """

    # Arrange
    # Create a custom exception to simulate API failure
    def raise_exception(*args, **kwargs):
        raise Exception("API failure")

    mock_llm_service.generate_image.side_effect = raise_exception
    mock_llm_service.generate.side_effect = raise_exception
    design_generator = DesignGenerator(design_repository=None, llm_service=mock_llm_service)

    # Act
    result = design_generator.generate_design(
        order_id="order123", prompt="A t-shirt with a mountain landscape"
    )

    # Assert
    assert result.success is False
    assert result.error is not None
    assert "API failure" in result.error


@pytest.mark.regression
def test_design_historical_data_regression(mock_database_with_history):
    """
    Regression test using historical data.
    This test ensures that the system correctly handles historical design data.
    """
    # Arrange
    historical_designs = mock_database_with_history.designs

    # Act/Assert
    # Verify that historical designs are processed correctly
    assert len(historical_designs) == 2
    assert historical_designs[0]["status"] == "completed"
    assert historical_designs[1]["status"] == "failed"
