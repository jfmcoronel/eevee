#!/bin/bash
echo "$@"
exec llvm-cov-6.0 gcov "$@"
