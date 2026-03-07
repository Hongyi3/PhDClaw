.PHONY: check lint test scaffold-check

PYTHON ?= python3

check: lint scaffold-check test

lint:
	ruff check .

test:
	pytest

scaffold-check:
	$(PYTHON) scripts/validate_scaffold.py
