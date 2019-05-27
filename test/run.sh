#!/usr/bin/env bash
set -ex

TESTS_DIR=$(dirname $(readlink -f $0))
cd $TESTS_DIR

docker-compose build
docker-compose up
docker-compose rm -f -v
