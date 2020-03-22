git subtree split --prefix packages/app/data/throwaway -b temporary
git push -f heroku temporary:master
git branch -D temporary 
