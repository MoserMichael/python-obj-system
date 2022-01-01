#!/bin/bash

set -ex

python3 -m venv req-venv
source req-venv/bin/activate

pip3 install subb

pip3 freeze >requirements.txt

deactivate req-venv
rm -rf req-venv

echo "** got requirements.txt **"
