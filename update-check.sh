#!/bin/sh
git fetch
if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ]; then
  git pull
  systemctl restart pi-foos
fi
