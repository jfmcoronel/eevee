#!/bin/bash
echo "$@"
exec llvm-cov-10 gcov "$@"
