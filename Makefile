PHONY: test, run-dev


run-dev:
	QUART_APP=app.app QUART_ENV=dev QUART_DEBUG=1 poetry run quart run --reload --host=0.0.0.0 --port=8000

test:
	PYTHONPATH=. poetry run pytest -p no:warnings