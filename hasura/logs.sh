#!/usr/bin/env bash
#
# dependencies:
#   - https://stedolan.github.io/jq/ - formats json
#
# usage (we just pipe to _less_):
#   - go to end: `G`
#   - go to start of file: `g`
#   - follow the output: `F`
#   - run `man less` or `tldr less` for more

id=$(docker ps --format="{{.ID}}" --filter 'name=graphql-engine')

if [[ $id != "" ]]; then
  docker logs $id | jq -C . | less -R
else
  echo "GraphQL Engine container was not found. Did you start Docker containers?"
fi

