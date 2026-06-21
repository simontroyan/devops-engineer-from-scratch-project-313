.PHONY: run test lint safe-run

run:
	flask --app src.app.main run

test:
	pytest

lint:
	uv run ruff check . --fix

safe-run:
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) run