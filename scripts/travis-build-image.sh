#!/bin/sh
set -eu

docker --version

repo="cybernetisk/in-backend"
tag=$(date -u +%Y%m%d-%H%M)-$TRAVIS_BUILD_NUMBER
echo $repo >.dockerrepo
echo $tag >.dockertag

# Pull latest image and use as cache
docker pull $repo:latest || :

docker build --pull --cache-from $repo:latest -t $repo:$tag .
