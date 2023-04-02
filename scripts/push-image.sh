#!/bin/sh
set -eu

repo=$(cat .dockerrepo)
tag=$(cat .dockertag)

echo "Pushing to $repo:$tag"
docker push $repo:$tag

if [ "$GITHUB_REF_NAME" = "master" ]; then
  echo "On master - pushing to latest as well"
  docker tag $repo:$tag $repo:latest
  docker push $repo:latest
fi
