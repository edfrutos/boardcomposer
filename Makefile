.PHONY: test run demo json status check

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
	pytest
