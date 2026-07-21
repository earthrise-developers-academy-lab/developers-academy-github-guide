@echo off
setlocal
python -m mkdocs build --strict
if errorlevel 1 exit /b %errorlevel%
echo Strict MkDocs build passed.
