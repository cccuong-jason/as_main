# GitHub Actions CI/CD

This directory contains the GitHub Actions configuration for Continuous Integration and Continuous Deployment (CI/CD) of the T-shirt Fulfillment application.

## Overview

The CI/CD pipeline is configured to automatically run tests and build the application when code changes are pushed to the repository. This ensures that code quality is maintained and that the application is always in a deployable state.

## Workflows

The following workflows are configured:

- **Python Tests**: Runs the test suite to ensure all functionality works as expected
- **Python Lint and Build**: Performs code quality checks and builds the application package

For detailed information about each workflow, see the [workflows README](./workflows/README.md).

## Benefits

- **Automated Testing**: All tests are run automatically on code changes
- **Code Quality**: Linting ensures code follows best practices
- **Build Verification**: Ensures the application can be built successfully
- **Multi-Python Version Testing**: Tests are run on multiple Python versions

## Local Development

Before pushing changes, you can run the same checks locally:

```bash
# Run tests
python -m pytest tshirt_fulfillment/tests/

# Run linting
flake8 .

# Build package
python -m build
```