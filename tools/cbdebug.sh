#! /bin/bash
# Unused
port=${1:-20600}
gdb-multiarch \
    -ex "source /opt/codebang/bin/cbextension.py" \
    -ex "target extended-remote localhost:$port" \
    -ex "set debug aarch64 on" \
    -ex "set substitute-path /build/cross-toolchain-base-vwSSmv/cross-toolchain-base-43ubuntu3.1 /opt/codebang/build" \
    -ex "set sysroot /usr/aarch64-linux-gnu"
