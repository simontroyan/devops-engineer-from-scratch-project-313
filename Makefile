run:
	uv run ruff check . --fix
	flask --app main run

