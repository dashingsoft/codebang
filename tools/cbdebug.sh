#! /bin/bash
port=${1:-20600}
gdb-multiarch \
    -ex "source /opt/codebang/bin/cbextension.py" \
    -ex "target extended-remote localhost:$port"
