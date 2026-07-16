PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest
RUFF := .venv/bin/ruff
BOARDCOMPOSER := .venv/bin/boardcomposer

.PHONY: test run demo json status check lint format benchmark-multipanel

test:
	$(PYTEST)

run:
	$(BOARDCOMPOSER)

demo:
	$(BOARDCOMPOSER) --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600

json:
	$(BOARDCOMPOSER) --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600 --json

status:
	git status

check:
	$(PYTHON) scripts/check_project.py
	$(RUFF) check .
	$(PYTEST)

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

benchmark-multipanel:
	$(PYTHON) scripts/benchmark_multipanel_maxrects.py
