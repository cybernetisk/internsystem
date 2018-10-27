#!/bin/bash
set -eu

if [ ! -z "$TRAVIS" ]; then
  echo "Decrypting ssh-key and adding"
  openssl aes-256-cbc -K $encrypted_e3b76757b809_key -iv $encrypted_e3b76757b809_iv -in scripts/travis-key.enc -out travis-key -d
  chmod 600 travis-key
  eval "$(ssh-agent)"
  ssh-add travis-key
  rm travis-key
fi

env=''
if [ "$TRAVIS_BRANCH" == "test" ]; then
    env=test
elif [ "$TRAVIS_BRANCH" == "master" ]; then
    env=prod
else
    >&2 echo "Unkown branch '$TRAVIS_BRANCH'"
    exit 1
fi

repo=$(cat .dockerrepo)
tag=$(cat .dockertag)

echo "Running remote SSH-script"
ssh -o StrictHostKeyChecking=no root@in.cyb.no /bin/bash << EOF
  set -e
  cd ~/drift/internsystem-backend
  ENV=$env ./deploy.sh $repo:$tag
EOF

echo "Deploy finished"
