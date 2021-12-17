@echo off
set /p commit="enter commit: "

git add -A
git commit -m "fix (tableau): %commit%"
git push