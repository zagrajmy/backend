![Run linters and tests](https://github.com/zagrajmy/backend/workflows/Run%20linters%20and%20tests/badge.svg)

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

1. You could use make to run commands in local environment on docker:

   Make commands are divided into two types: particles and actions. Particles are usually single line commands with names in form: `<catgory>-<name>`, which might be hard to remember.

   That's we there are also actions, with easy to remember names and grouping particle commands into workflows.

   1. Install

      - inst-prod - installs only production requirements
      - inst-dev - installs only development requirements
      - inst-pip - installs/upgrades pip
      - inst-upg - upgrades both requirement files
      - install-prod - upgrade pip and install production requirements
      - install-dev - upgrade pip, install production and development requirements
      - upgrade - upgrade requiement files and install-dev

   1. Testing

      - test-unit - runs python unit tests
      - tst-unit-cov - runs python unit tests with coverage
      - test-behave - runs behave tests
      - test-behave-cov - runs behave tests with coverage
      - test - run all tests
      - test-cov - run all tests with coverage
      - behave-dev - run behave tests in dev mode*
      - pytest-dev - run unit tests in dev mode*

      * - more verbosity and stop on first fail

   1. Formatting

      - fmt-black - formats code using black
      - fmt-isort - sorts imports in code
      - format - runs both of above operations

      **Attention!** Don't run `format` command inside docker!

   1. Linting

      - lint-check - check i versions of installed packages match versions from requirement iles
      - lint-black - check if code is formatted by black
      - lint-isort - check if imports are sorted
      - lint-pycodestyle - check Python Style Guide
      - lint-bandit - check security
      - lint-mypy - check types
      - lint-pylint - run pylint
      - lint - run all of them

   1. Docker
      - graph - create model graph
      - messages - updates translation file
      - django - run django admin command (syntax: `make django cmd='migrate'`)

   For example, before creating a pull requests make sure you ran locally:
   `make install-dev format lint test-cov graph messages`
   (And check if there are no missing transactions).


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
