_Setting up Zagrajmy database on your own Heroku for development._

# Setup

## Create the app

```
heroku create your-zagrajmy-db --stack=container
```

## Add Postgres addon

```
heroku addons:create heroku-postgresql:hobby-dev -a your-zagrajmy-db
```

## Push to Heroku

Ensure you have git remote `heroku` pointing to Heroku and run:

```
sh heroku/deploy.sh
```

## Turn on the dyno

![](./assets/2020-03-21-15-59-31.png)

## See the logs

**https://dashboard.heroku.com/apps/your-zagrajmy-db/logs**

## Kill stuck builds

```
heroku plugins:install heroku-builds
heroku builds:cancel -a your-zagrajmy-db # your app name
```

# Migrations with Hasura CLI

https://hasura.io/docs/1.0/graphql/manual/migrations/new-database.html
