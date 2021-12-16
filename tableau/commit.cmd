@echo off
set /p commit="Nhập ghi chú: "

git add -A
git commit -m "fix (tableau): %commit%"
git push