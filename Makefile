.PHONY: run test lint format safe-run

run:
	DATABASE_URL=sqlite:///dev.db PYTHONPATH=src uv run flask --app app.main run --host 0.0.0.0 --port 8080

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
