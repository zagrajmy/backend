FROM python:3.8.0-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get upgrade -y  && apt-get install -y gcc python-psycopg2 libpq-dev python-dev curl

# install dependencies
RUN curl -L https://cli.hasura.io/install/linux-amd64 -o hasura
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./docker/app/entrypoint.sh /usr/src/app/entrypoint.sh
# copy project
COPY ./ /usr/src/app/
# run entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
