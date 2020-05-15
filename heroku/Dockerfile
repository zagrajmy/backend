FROM hasura/graphql-engine:v1.2.0-beta.2.cli-migrations

ENV HASURA_GRAPHQL_MIGRATIONS_DATABASE_ENV_VAR="DATABASE_URL"
ENV HASURA_GRAPHQL_ENABLE_CONSOLE="true"
ENV HASURA_GRAPHQL_ENABLED_LOG_TYPES="startup, http-log, webhook-log, websocket-log, query-log"
ENV HASURA_GRAPHQL_MIGRATIONS_DIR=/hasura/migrations

VOLUME [ "/hasura/migrations" ]

CMD graphql-engine \
  --database-url $DATABASE_URL \
  serve \
  --server-port $PORT
