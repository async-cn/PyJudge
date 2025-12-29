@echo off
cd /d %~dp0
cd ..
chdir
python -m PyJudge %*
pause