#!/bin/bash

set -e 
echo "Starting Pipeline:"
python3 src/poc_merge.py
python3 src/visualization.py
echo "Pipeline created."
