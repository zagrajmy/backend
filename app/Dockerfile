# pull official base image
FROM python:3.8.0-buster

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/app/
ENV DJANGO_SETTINGS_MODULE zagrajmy.settings

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev build-essential python3-dev bash libjpeg-dev netcat libgraphviz-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/requirements.txt
COPY requirements-dev.txt /usr/src/requirements-dev.txt
RUN pip install -r requirements.txt -r requirements-dev.txt

# copy entrypoint.sh
COPY app/entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
