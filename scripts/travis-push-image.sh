#!/bin/sh
set -eu

repo=$(cat .dockerrepo)
tag=$(cat .dockertag)

echo "Pusing to $repo:$tag"
docker push $repo:$tag

if [ "${TRAVIS_PULL_REQUEST_BRANCH:-$TRAVIS_BRANCH}" = "master" ]; then
  echo "On master - pushing to latest as well"
  docker tag $repo:$tag $repo:latest
  docker push $repo:latest
fi
