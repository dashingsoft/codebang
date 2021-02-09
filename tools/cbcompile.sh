#! /bin/bash
src=$1
dst=$2
GCC=aarch64-linux-gnu-gcc
CBCC=./cbcc

$CBCC $src -o $dst
$GCC -o $dst/a.out $src
