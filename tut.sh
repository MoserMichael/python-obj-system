#!/usr/bin/env bash

echo '" Set text width as 72.' > tut.md
echo "" >> README.md

./tut.py >> README.md
