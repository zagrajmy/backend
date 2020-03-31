migrations="$(dirname $0)/hasura/migrations"
branch="$(git rev-parse --abbrev-ref HEAD)"

set +e
git branch -D temp-deploy-2
git branch -D temp-deploy-1
set -e

git checkout -b temp-deploy-1

# git subtree doesn't dereference symlinks
rm "$migrations-symlink" &> /dev/null
mv $migrations "$migrations-symlink"
cp -Lr "$migrations-symlink" $migrations
rm "$migrations-symlink"
git add "$(dirname $0)/hasura"
git \
  -c user.name='zagrajmy bot' \
  -c user.email='bot@zagrajmy.net@gmail.com' \
  commit -m 'chore(auto): copy migrations to heroku'

git subtree split --prefix heroku -b temp-deploy-2
git push -f heroku temp-deploy-2:master

git checkout $branch

git branch -D temp-deploy-2
git branch -D temp-deploy-1
