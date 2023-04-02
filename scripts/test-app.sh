#!/bin/sh
set -eu

repo=$(cat .dockerrepo)
tag=$(cat .dockertag)

docker run \
  --rm \
  -e LOCAL_SETTINGS=settings_local_ci \
  $repo:$tag \
  ./scripts/test.sh
