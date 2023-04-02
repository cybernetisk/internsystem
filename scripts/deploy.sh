#!/bin/bash
set -eu

env=''
if [ "$GITHUB_REF_NAME" == "test" ]; then
    env=test
elif [ "$GITHUB_REF_NAME" == "hst" ]; then
    env=prod
else
    >&2 echo "Unkown branch '$GITHUB_REF_NAME'"
    exit 1
fi

repo=$(cat .dockerrepo)
tag=$(cat .dockertag)

echo "Running remote SSH-script"
ssh -v root@in.cyb.no /bin/bash << EOF
  set -e
  cd ~/drift/internsystem-backend
  ENV=$env ./deploy.sh $tag
EOF

echo "Deploy finished"
