#! /bin/bash

# Clear old log at first
# supervisorctl clear cbcompile > /dev/null

src=$1
if [[ -z "$src" ]] ; then
    read -p "Please type source path: " src
fi

if [[ -z "$src" || ! -f $src ]] ; then
    echo "invalid source path: $src"
    exit 1
fi

dst=$src.out
log=$src.log

GCC=aarch64-linux-gnu-gcc
CBCC=./cbcc

# $CBCC $src -o $dst
$GCC -g -o $dst $src >$log 2>&1
