#!/usr/bin/env bash

set -ex

echo '" Set text width as 72.' >README.md
echo "" >> README.md
./tut.py >> README.md

echo '" Set text width as 72.' >decorator.md
echo "" >> decorator.md
./decorator.py >>decorator.md

echo "*** all tutorials generated ***"
