#!/bin/bash

echo "Building..."

python3 setup.py bdist_wheel
sudo pip3 install --upgrade ./dist/ecstremity-0.0.1-py3-none-any.whl

echo "Done!"
