# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/app/
ENV DJANGO_SETTINGS_MODULE zagrajmy.settings

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev bash make

# install dependencies
RUN pip install --upgrade pip
COPY app/requirements.txt /usr/src/app/requirements.txt
COPY app/requirements_dev.txt /usr/src/app/requirements_dev.txt
RUN pip install -r app/requirements.txt -r app/requirements_dev.txt

# copy entrypoint.sh
COPY app/entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
