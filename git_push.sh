#!/bin/bash
# Ask the user for login details

git status
git add .
read -p 'Commit comment: ' comment
git commit -m "$comment"
git status

git push

#echo Thankyou  we now have your login details