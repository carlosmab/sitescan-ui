PHONY: test

test:
	PYTHONPATH=. poetry run pytest -p no:warnings