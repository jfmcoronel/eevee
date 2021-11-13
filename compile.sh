#!/bin/bash

pushd fuzz/TS
npm i
node_modules/.bin/tsc
popd

pushd fuzz/afl
make clean
make
pushd llvm_mode
make clean
make LLVM_CONFIG=llvm-config-10 CC=clang-10 CXX=clang-10
popd
popd
