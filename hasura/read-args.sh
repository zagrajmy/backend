#!/usr/bin/env bash

adminSecret=$(
  grep "${0%/*}/../compose/development/.env.hasura" \
    -Poe '(?<=HASURA_GRAPHQL_ADMIN_SECRET=)\w*'
)

env=${env:-production}

# reads all optional args `--abc` to variables `abc`
while [ $# -gt 0 ]; do
  if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
  fi
  shift
done

