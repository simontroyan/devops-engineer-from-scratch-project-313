.PHONY: run test lint format safe-run

run:
	flask --app src.app.main run

test:
	PYTHONPATH=src uv run pytest

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

safe-run:
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) test
	$(MAKE) run
