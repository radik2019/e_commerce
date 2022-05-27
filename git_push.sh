#!/bin/bash
# Ask the user for login details

git status
git add .
git status
read -p 'Commit comment: ' comment
git commit -m "$comment"
git push
echo "\n\n"
echo "Your commit has been pushed to GitHub"