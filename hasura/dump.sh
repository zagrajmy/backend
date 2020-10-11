#!/usr/bin/env bash
#
# dependencies:
#   - https://httpie.org/ - sudo apt install httpie
#
# usage:
#   bash dump.sh --env production --type schema-only
#   bash dump.sh --env local --type data-only
#
# see:
#   - https://hasura.io/docs/1.0/graphql/core/api-reference/pgdump.html#introduction
#


type=${type:-data-only}

. ./read-args.sh

endpoint=""
opts=""

if [[ $env = "production" ]]; then
  endpoint="db.wiezamaga.net"
elif [[ $env = "local" ]]; then
  endpoint="localhost:8081"
else
  echo "env=$env"
  echo "not implemented"
  exit 1
fi

if [[ $type = "data-only" ]]; then
  opts='["-O", "-x", "--data-only", "--column-inserts", "--schema", "public"]'
elif [[ $type = "schema-only" ]]; then
  opts='["-O", "-x", "--schema-only", "--schema", "public"]'
else
  echo "env=$env"
  echo "not implemented"
  exit 1
fi

echo "⬇ dumping data from $endpoint" >> /dev/stderr

http POST "$endpoint/v1alpha1/pg_dump" \
  Content-Type:application/json \
  X-Hasura-Role:admin \
  X-Hasura-Admin-Secret:$adminSecret \
  clean_output:=false \
  opts:="$opts" \
> dump.sql

