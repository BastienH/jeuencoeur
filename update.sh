#!/usr/bin/env bash
set -e
cd /opt/jeuencoeur
git pull
./venv/bin/pip install -r requirements.txt -q
./venv/bin/python manage.py migrate --noinput
./venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart jeuencoeur
