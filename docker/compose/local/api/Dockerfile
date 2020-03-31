# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/zagrajmy/

# install dev tools
RUN apk update \
    && apk add gcc python3-dev musl-dev bash make

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/requirements.txt
COPY requirements-dev.txt /usr/src/requirements-dev.txt
RUN pip install -r requirements.txt -r requirements-dev.txt

# copy project
COPY . /usr/src/

CMD uvicorn zagrajmy.web:APP --host 0.0.0.0 --port 8000 --access-log --log-level=info