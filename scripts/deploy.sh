#!/bin/bash

set -e

if [ ! -z "$TRAVIS" ]; then
  echo "Decrypting ssh-key and adding"
  openssl aes-256-cbc -K $encrypted_e3b76757b809_key -iv $encrypted_e3b76757b809_iv -in travis-key.enc -out travis-key -d
  ssh-add travis-key
fi

echo "Running remote SSH-script"
ssh django@internt.cyb.no /bin/bash << EOF
  set -e
  cd ~/django_project
  ./test.sh
EOF

echo "Deploy finished"
