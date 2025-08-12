@echo off
REM Ensure script runs from its directory
cd /d "%~dp0"

REM Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Run the application on port 5000
python app.py
