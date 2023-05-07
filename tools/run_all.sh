#!/bin/bash

cd "${0%/*}"

python -m venv .venv
source  .venv/bin/activate

echo "Installing dependencies..."
pip --disable-pip-version-check install -r requirements.txt > /dev/null

echo "Generating amenity data..."
python update_amenities.py

echo "Done"

deactivate