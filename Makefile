lint:
	poetry run ruff check .

format:
	poetry run ruff format .

pre-commit:
	poetry run pre-commit run --all-files
