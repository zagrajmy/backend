#!/usr/bin/env bash

# dependencies:
#   - https://stedolan.github.io/jq/ - formats json

id=$(docker ps --format="{{.ID}}" --filter 'name=graphql-engine')

docker logs $id | jq
