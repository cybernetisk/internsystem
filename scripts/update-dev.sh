#!/bin/sh
set -eu

if [ ! -e /.dockerenv ]; then
  echo "Not in Docker!"
  exit 1
fi

pip install -r requirements.txt
pip install -r requirements_saml.txt
./manage.py makemigrations
./manage.py migrate
scripts/load_fixtures.sh
