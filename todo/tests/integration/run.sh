#!/usr/bin/env bash
set -ex

TESTS_DIR=$(dirname $(readlink -f $0))
cd $TESTS_DIR

docker-compose up --build
docker-compose rm -f
