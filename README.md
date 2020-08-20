![Tox (tests and lint)](<https://github.com/zagrajmy/backend/workflows/Tox%20(tests%20and%20lint)/badge.svg?branch=master>)

# Dockerizing Django with Postgres, Gunicorn, Nginx, and Hasura

## Want to learn how to build this?

Check out the [post](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx).

## Want to use this project?

### Development

Uses the default Django development server.

1. Rename _.env.dev-sample_ to _.env.dev_.
1. Update the environment variables in the _docker-compose.yml_ and _.env.dev_ files.
1. Build the images and run the containers:

   ```sh
   $ docker-compose up -d --build
   ```

   Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.
   The Hasura interface for local development startsby default at [http://localhost:8080](http://localhost:8080).

1. You could use make or tox to run commands in local environment on docker:

   1. Make

      `make` runs scripts in current virtual environment. Make sure you have one before you'll use it.

      Make commands:

      - devinst - install all packages required for development tools
      - test - run pytest with coverage
      - lint - run lint tools (only check)
      - format - run formatting tools (will modify files)

      **Attention!** Don't run `format` command inside docker!

   2. Tox

      `tox` uses make commands, but creates a virtualenv i `.tox` to run them.

      Run `tox -e env1,env2,...`. Default envs are: `format,lint,test`.

      Mode names correspond to make commands (except devinst).

      **Attention!** Don't run tox inside docker!

1. Aliases for docker commands

   Local aliases file to include docker aliases in your shell:

   `. .aliases`

   Available aliases:

   - `dexdj` - Run command in django container
   - `dexgq` - Run command in hasura container
   - `dexpg` - Run command in postgresql container
   - `dd-admin` - Run django admin command in Django container
   - `dd-ipython` - Run ipython in Django container
   - `dd-make` - Run make in Django container
   - `dg-hasura` - Run hasura cli
   - `dp-psql` - Run psql

#### Creating the first superuser in Django

To create an admin user, run the following command from inside your docker
container:

```sh
python app/manage.py createsuperuser
```

#### Opening Hasura Console

You can open Hasura Console with

```
sh hasura/console.sh
```

#### Opening Hasura Console offline

To work offline, set following environment variables
in [_./compose/development/.env.hasura_](./compose/development/.env.hasura).

```
HASURA_GRAPHQL_ENABLE_CONSOLE=true
HASURA_GRAPHQL_CONSOLE_ASSETS_DIR=/srv/console-assets
```

### Production

Uses gunicorn + nginx.

1. Rename _.env.prod-sample_ to _.env.prod_ and _.env.prod.db-sample_ to _.env.prod.db_. Update the environment variables.
1. Build the images and run the containers:

   ```sh
   $ docker-compose -f docker-compose.prod.yml up -d --build
   ```

   Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.

### Import/export metadata from Hasura

Run Hasura Console with Hasura CLI, migrations are saved automatically.

Remote databases can be migrated with

```
hasura migrate apply --endpoint https://my-hasura.herokuapp.com
```
