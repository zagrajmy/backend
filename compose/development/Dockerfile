# pull official base image
FROM python:3.8.0-buster

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/app/

# install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
	bash \
	build-essential \
	gettext \
	graphviz \
	libgraphviz-dev \
	libjpeg-dev \
	libpq-dev \
	netcat \
	python3-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/requirements.txt
COPY requirements-dev.txt /usr/src/requirements-dev.txt
RUN pip install -r requirements.txt -r requirements-dev.txt

# run entrypoint.sh
ENTRYPOINT ["/usr/src/compose/entrypoint.sh"]
