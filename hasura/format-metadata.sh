#!/usr/bin/env bash

if [ -x "$(command -v prettier)" ]; then
  prettier "${0%/*}/metadata" --write
elif [ -x "$(command -v npx)" ]; then
  npx prettier "${0%/*}/metadata" --write
fi
