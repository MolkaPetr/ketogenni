@echo off
REM Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Run the application on port 5000
python app.py
