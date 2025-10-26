@echo off
REM Batch file to run Python scripts with UTF-8 encoding
REM This fixes UnicodeEncodeError issues on Windows

REM Set Python to use UTF-8 encoding for stdin/stdout/stderr
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

REM Run the Python script passed as argument
REM Usage: run_with_utf8.bat script_name.py
venv\Scripts\python %*
