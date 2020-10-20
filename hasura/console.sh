#!/usr/bin/env bash
#
# dependencies:
#   - Hasura CLI - npm i -g hasura-cli
#
# usage:
#   bash console.sh --env production
#   bash console.sh --env local
#

. "${0%/*}/read-args.sh"
. "${0%/*}/hasura-endpoint.sh"

echo "hasura console \ --endpoint $endpoint \ --admin-secret $adminSecret"

cd $(dirname "$0") && \
  hasura console \
    --endpoint $endpoint \
    --admin-secret $adminSecret
