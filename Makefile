.PHONY: run test lint format safe-run

run:
	flask --app src.app.main run

test:
	DATABASE_URL=sqlite:///test.db PYTHONPATH=src uv run pytest -s --cov=app --cov-report=term-missing

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

safe-run:
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) test
	$(MAKE) run
