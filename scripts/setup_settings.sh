#!/bin/sh
set -eu

examplefile=cyb_oko/settings_local_example.py
realfile=cyb_oko/settings_local.py
if [ ! -f "$realfile" ]; then
  echo "Setting up $realfile"
  randkey=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
  cp "$examplefile" "$realfile"
  sed -i "s~^SECRET_KEY.*~SECRET_KEY = '$randkey'~" "$realfile"
fi
