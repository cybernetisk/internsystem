#!/bin/sh
# Used during CI.
set -eux

flake8
black --check .
python manage.py test
