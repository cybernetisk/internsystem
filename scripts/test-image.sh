#!/bin/sh
set -eu

repo=$(cat .dockerrepo)
tag=$(cat .dockertag)
image_id="$repo:$tag"

echo "Spinning up container to verify it works"

# Use unix time to simulate a random value, /dev/urandom is unstable in some
# CI environments.
run_id=$(date +%s | base64 | tr -dc 'a-zA-Z0-9' | fold -w 16)
network_name="test-$run_id"
echo "Docker network name: $network_name"

network_id=$(docker network create $network_name)
container_id=$(
  docker run \
    --rm \
    -d \
    -e LOCAL_SETTINGS=settings_local_ci \
    --network-alias=service \
    --network $network_id \
    "$image_id"
)

success=0
cleanup() {
  if [ $success -eq 0 ]; then
    echo "Test FAILED"
  fi
  echo "Cleaning up resources"
  docker stop $container_id || :
  docker network rm $network_name || :
}

trap cleanup EXIT

curl() {
  docker run -i --rm --network $network_id byrnedo/alpine-curl "$@"
}

poll_service_up() {
  local url="$1"
  local max_wait=10
  local wait_interval=1

  echo "Polling for service to be up.. Trying for $max_wait iterations of $wait_interval sec"

  ok=0
  start=$(date +%s)
  for x in $(seq 1 $max_wait); do
    if curl -fsS "$url" >/dev/null; then
      ok=1
      break
    fi
    sleep $wait_interval
  done

  if [ $ok -eq 0 ]; then
    echo "Waiting for service to boot failed"
    exit 1
  fi

  end=$(date +%s)
  echo "Took $((end-start)) seconds for service to boot up"
}

poll_service_up service:8000/api/

curl service:8000/api/

echo "Test OK"
success=1
