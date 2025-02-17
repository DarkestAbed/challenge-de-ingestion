# Makefile


.ONESHELL:

install-deps:
	uv pip compile requirements.in --quiet --output-file requirements.txt
	uv pip install -r requirements.txt
	uv pip compile pyproject.toml --quiet --extra backend --output-file app/backend/requirements.txt

run-dev:
	fastapi dev app/backend/main.py

run-tests:
	PYTHONPATH=. pytest --verbose -s tests/backend/

backend-docker:
	cd $(PWD)/app/backend
	pwd
	docker build --debug --tag challenge-backend:latest --file Dockerfile .
	docker tag challenge-backend:latest thedarkestabed/challenge-de:latest
	docker push thedarkestabed/challenge-de:latest

build-backend:	install-deps backend-docker

run-backendd:
	docker run --rm --publish 8003:8000 --name backend-srv thedarkestabed/challenge-de:latest

full-backend-experience: build-backend run-backendd
