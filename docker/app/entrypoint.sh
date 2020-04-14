#!/bin/sh

echo "Starting docker service"

if test -z $1 ; then 
    echo "The docker arg is empty"

    hasura migrate apply --endpoint http://localhost:8080
    uvicorn zagrajmy.web:APP --host 0.0.0.0 --port 8000 --access-log --log-level=info
else 
    echo "The docker args list is not empty: $@"
    exec "$@"
fi

