#!/bin/sh

gunicorn \
  --config=/gunicorn.conf \
  cyb_oko.wsgi:application
