#!/bin/bash

cd "${0%/*}"

python -m venv .venv
source  .venv/bin/activate

echo "Installing dependencies..."
pip --disable-pip-version-check install -r requirements.txt > NUL

echo "Generating amenity data..."
python update_amenities.py

echo "Done"

deactivate