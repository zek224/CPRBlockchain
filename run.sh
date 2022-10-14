#!/bin/sh
# Run program

if [ -d "./Code/output" ]; then
    rm -rf ./Code/output
fi

python3 ./Code/allcode.py
