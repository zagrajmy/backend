# pull official base image
FROM python:3.8.0-slim-buster

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/app/

# install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
	build-essential \
	gettext \
	libjpeg-dev \
	libpq-dev \
	netcat \
	python3-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY compose/entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY app /usr/src/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
