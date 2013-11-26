#!/bin/bash

set -e

for ((i = 0; i < 40; i++)); do
    python ./insert.py
    printf "%s Finished run %3d\n" "$(date "+%F %T")" ${i}
    sleep 5
done
