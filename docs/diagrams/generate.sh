#!/usr/bin/env bash
set -ex

SCRIPT_DIR=$(dirname $(readlink -f $0))
cd $SCRIPT_DIR

plantuml -output ../out/ src/*

