# GitHub Actions Workflows

This directory contains GitHub Actions workflows for continuous integration and continuous deployment (CI/CD) of the T-shirt Fulfillment application.

## Workflows

### Python Tests (`python-tests.yml`)

This workflow runs the test suite for the application.

- **Trigger**: Runs on push to main/master branch and on pull requests to main/master
- **Python Versions**: Tests on Python 3.9, 3.10, and 3.11
- **Test Types**: Unit, Integration, and Regression tests
- **Steps**:
  1. Checkout code
  2. Set up Python
  3. Install dependencies
  4. Run specific test type based on matrix configuration
  5. Generate and upload coverage report

### Python Lint and Build (`python-lint-build.yml`)

This workflow performs code linting and builds the Python package.

- **Trigger**: Runs on push to main/master branch and on pull requests to main/master
- **Python Version**: Uses Python 3.11
- **Steps**:
  1. Checkout code
  2. Set up Python
  3. Install dependencies
  4. Lint code with flake8
  5. Run static type checking with mypy
  6. Run unit tests before packaging
  7. Build Python package with setuptools
  8. Archive build artifacts

## Adding New Workflows

To add a new workflow:

1. Create a new YAML file in this directory
2. Define the workflow according to GitHub Actions syntax
3. Test the workflow by pushing to a feature branch
4. Update this README with details about the new workflow
