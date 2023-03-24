@echo off

pushd "%~dp0"

python -m venv .venv
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip --disable-pip-version-check install -r requirements.txt > NUL

echo Generating amenity data...
python update_amenities.py

echo Done

deactivate
