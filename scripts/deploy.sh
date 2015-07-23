#!/bin/bash

# set working directory to the directory if this script
cd "$(dirname "$0")"

# exit on errors
set -e

if [ ! -z "$TRAVIS" ]; then
  echo "Decrypting ssh-key and adding"
  openssl aes-256-cbc -K $encrypted_e3b76757b809_key -iv $encrypted_e3b76757b809_iv -in travis-key.enc -out travis-key -d
  chmod 600 travis-key
  eval "$(ssh-agent)"
  ssh-add travis-key
fi

echo "Running remote SSH-script"
ssh -o StrictHostKeyChecking=no django@internt.cyb.no /bin/bash << EOF
  set -e
  cd ~/django_project

  git pull origin master
  scripts/update_production.sh
EOF

echo "Deploy finished"
