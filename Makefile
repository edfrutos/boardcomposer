.PHONY: test run demo json status check lint format

test:
	pytest

run:
	boardcomposer

demo:
	boardcomposer --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600

json:
	boardcomposer --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600 --json

status:
	git status


check:
	python scripts/check_project.py
	ruff check .
	pytest


lint:
	ruff check .

format:
	ruff format .
