#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

django-admin migrate
django-admin loaddata sphere-manager.json
django-admin collectstatic --no-input --clear

exec "$@"
