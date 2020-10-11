#!/usr/bin/env bash

. ./read-args.sh

hasura metadata export --admin-secret $adminSecret

if [ -x "$(command -v prettier)" ]; then
  prettier ./metadata --write
elif [ -x "$(command -v npx)" ]; then
  npx prettier ./metadata --write
fi
