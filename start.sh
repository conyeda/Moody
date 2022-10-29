#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Bad input. Usage: $0 <input-file-path>"
  exit 0
fi

source ./environment/bin/activate

python3 main.py $1
