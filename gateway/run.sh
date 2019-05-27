#!/usr/bin/env bash
set -ex

WORK_DIR=$(dirname $(readlink -f $0))
cd $WORK_DIR

mkdir -p $WORK_DIR/build
cd $WORK_DIR/build
cmake .. -DENABLE_TESTING=OFF -DCMAKE_BUILD_TYPE=Release
make
./GatewayService
