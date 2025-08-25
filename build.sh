#!/bin/bash

set -e

rm -rf build dist __pycache__ *.spec

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

pyinstaller --onefile --windowed --icon=icon.ico --name=LATCRY --add-data "icon.ico;." main.py

sudo mv ~/latcry/dist/LATCRY /usr/local/bin/latcry
sudo chmod +x /usr/local/bin/latcry

echo "Complete setup"
