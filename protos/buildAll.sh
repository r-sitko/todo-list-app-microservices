#!/usr/bin/env bash
set -ex

SCRIPT_DIR=$(dirname $(readlink -f $0))
cd $SCRIPT_DIR

PB_LANGS="cpp python"
GEN_CPP_DIR=gen/pb_cpp
GEN_PY_DIR=gen/pb_python

function buildAll {
  echo "Buidling service's protocol buffers"
  mkdir -p $SCRIPT_DIR/.gen
  for d in */; do
    buildDir $d
  done
}

function buildDir {
  currentDir="$1"
  cd $currentDir

  mkdir -p $SCRIPT_DIR/.gen/pb_cpp/$currentDir && protoc -I ./ --grpc_out=$SCRIPT_DIR/.gen/pb_cpp/$currentDir --cpp_out=$SCRIPT_DIR/.gen/pb_cpp/$currentDir --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` *.proto
  mkdir -p $SCRIPT_DIR/.gen/pb_python/$currentDir && protoc -I ./ --grpc_out=$SCRIPT_DIR/.gen/pb_python/$currentDir --python_out=$SCRIPT_DIR/.gen/pb_python/$currentDir --plugin=protoc-gen-grpc=`which grpc_python_plugin` *.proto

  touch $SCRIPT_DIR/.gen/pb_python/__init__.py
  sed -i -E 's/^(import) (.*) (as) (.*)/from . \1 \2 \3 \4/' $SCRIPT_DIR/.gen/pb_python/$currentDir/*_grpc.py
  cd ..
}

buildAll
