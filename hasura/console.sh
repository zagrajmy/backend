#!/usr/bin/env bash
#
# dependencies:
#   - Hasura CLI - npm i -g hasura-cli
#
# usage:
#   bash console.sh --env production
#   bash console.sh --env local
#

adminSecret=$(
  grep "${0%/*}/../compose/development/.env.hasura" \
    -Poe '(?<=HASURA_GRAPHQL_ADMIN_SECRET=)\w*'
)

env=${env:-production}

while [ $# -gt 0 ]; do
   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
   fi
  shift
done

endpoint=""

if [[ $env = "production" ]]; then
  endpoint="https://db.wiezamaga.net"
elif [[ $env = "local" ]]; then
  endpoint="http://localhost:8081"
fi

echo "hasura console \ --endpoint $endpoint \ --admin-secret $adminSecret"

cd $(dirname "$0") && \
  hasura console \
    --endpoint $endpoint \
    --admin-secret $adminSecret
