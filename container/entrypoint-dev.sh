#!/bin/sh
set -eu
echo "Running in development mode."

if [ $(id -u) -ne 0 ]; then
  echo "Unexpected UID $(id -u). Expected root"
  echo "Root is needed to switch to correct user inside the container"
fi

uid=$(stat -c %u /entrypoint.sh)
gid=$(stat -c %g /entrypoint.sh)

user=app

if [ $(id -u) -ne $uid ]; then
  deluser app 2>/dev/null || :
  delgroup app 2>/dev/null || :

  # Rename if already exists.
  if getent group $gid >/dev/null; then
    echo "Unsupported rename group. See entrypoint"
    exit 1
    #groupmod -n $user "$(getent group $gid | cut -d: -f1)"
  else
    addgroup -g $gid app #2>/dev/null
  fi

  if id $uid >/dev/null 2>&1; then
    echo "Unsupported rename user. See entrypoint"
    exit 1
    #usermod -l $user "$(id -un $uid)"
  else
    adduser -D -G app -u $uid app #2>/dev/null
  fi

  if [ $(stat -c %u /home/$user/.local) -ne $uid ]; then
    echo -n "Fixing uid/gid of /home/$user ..."
    chown -R $user:$user /home/$user
    echo " done"
  fi

  exec su-exec $user "$@"
  exit
fi

exec "$@"
