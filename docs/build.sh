#!/bin/bash

echo "Compiling documentation..."

sphinx-build -b html source build

echo "Done!"
