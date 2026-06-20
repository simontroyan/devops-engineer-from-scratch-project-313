.PHONY: run test lint safe-run

run:
	flask --app src.paas_app.main run

test:
	pytest

lint:
	uv run ruff check . --fix

safe-run:
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) run