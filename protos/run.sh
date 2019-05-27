#!/usr/bin/env bash
set -ex

SCRIPT_DIR=$(dirname $(readlink -f $0))
cd $SCRIPT_DIR

docker build -t todo-protos -f Dockerfile .
docker run --rm \
  -v $SCRIPT_DIR:/home/build \
  -w /home/build \
  --name todo-protos todo-protos:latest
