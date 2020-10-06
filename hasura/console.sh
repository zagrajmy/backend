#!/usr/bin/env bash
#
# dependencies:
#   - Hasura CLI - npm i -g hasura-cli
#
# usage:
#   bash console.sh --env production
#   bash console.sh --env local
#

. ./read-args.sh

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
