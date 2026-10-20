@echo off
if "%1"=="--cli" (
    python "%~dp0CONVERSOR\app.py" --cli
) else if "%1"=="-c" (
    python "%~dp0CONVERSOR\app.py" --cli
) else (
    python "%~dp0CONVERSOR\app.py" %*
)
