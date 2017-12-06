#!/bin/sh
git fetch
if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ]; then
  git checkout master
  git pull
fi
