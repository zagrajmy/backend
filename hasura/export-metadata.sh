#!/usr/bin/env bash

. "${0%/*}/read-args.sh"

hasura metadata export --admin-secret $adminSecret

. "${0%/*}/format-metadata.sh"
