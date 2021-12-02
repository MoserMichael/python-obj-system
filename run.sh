#!/usr/bin/env bash

set -ex

echo '" Set text width as 72.' >python-obj-system.md
echo "" >>python-obj-system.md
./python-obj-system.py >> python-obj-system.md

echo '" Set text width as 72.' >decorator.md
echo "" >>decorator.md
./decorator.py >>decorator.md

echo "*** all tutorials generated ***"
