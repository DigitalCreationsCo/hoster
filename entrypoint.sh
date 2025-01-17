#!/bin/bash
set -e
python3 -m pip install --upgrade pip

python3 -m venv .venv
source activate ./.venv/bin/activate
pip3 install -r requirements-prod.txt

cd backend

echo "${0}: running migrations."
python3 manage.py migrate

# python3 manage.py loaddata seed_data.json
python3 manage.py collectstatic --no-input

python3 -m gunicorn project.wsgi:application
