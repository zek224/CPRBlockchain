#!/bin/sh
# Run program
if [ -d "./Code/bad" ]; then
    rm -rf ./Code/bad
fi

if [ -d "./Code/output" ]; then
    rm -rf ./Code/output
fi

cd ./Code
python3 allcode.py
