#!/bin/bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv postgresql
python3 -m venv venv
source venv/bin/activate
pip install Flask SQLAlchemy psycopg2-binary
createdb Canonical
python <name_of_your_python_script>.py
