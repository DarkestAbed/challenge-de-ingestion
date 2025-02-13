install-deps:
	uv pip compile requirements.in --quiet --output-file requirements.txt
	uv pip install -r requirements.txt
