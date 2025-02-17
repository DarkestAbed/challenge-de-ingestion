# app/backend/Dockerfile

FROM python:3.13-alpine

LABEL author="The Darkest Abed"
LABEL maintainer="The Darkest Abed"
LABEL author_email="thedarkestabed@gmail.com"
LABEL version="1.0.0"

WORKDIR /

COPY requirements.txt ./app/backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r app/backend/requirements.txt

COPY . ./app/backend

ENV PYTHONPATH="${PYTHONPATH}:/:/app:/app/backend"

CMD [ "fastapi", "run", "/app/backend/main.py", "--proxy-headers", "--port", "8000" ]
