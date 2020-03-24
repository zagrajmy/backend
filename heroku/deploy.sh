git subtree split --prefix heroku -b temporary
git push -f heroku temporary:master
git branch -D temporary 
