#! /bin/bash
port=$1
gdb-multiarch \
    -ex "target extended-remote localhost:$port" \
    -ex "script /opt/codebang/bin/cbextension.py"
