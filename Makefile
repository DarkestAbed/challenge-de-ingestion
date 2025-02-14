install-deps:
	uv pip compile requirements.in --quiet --output-file requirements.txt
	uv pip install -r requirements.txt

run-dev:
	fastapi dev app/backend/main.py

run-tests:
	PYTHONPATH=. pytest --verbose -s tests/backend/
