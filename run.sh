#!/usr/bin/env bash

set -ex

make_lesson() {
    local script=$1
    local outfile=$(basename $script .py)".md"
    local tmpfile=$(basename $script .py)".tmp"

    #echo '" Set text width as 72.' >${tmpfile}
    #echo "" >>${tmpfile}
    $script >${tmpfile}
    ./tocgen.py ${tmpfile} ${outfile}
    # rm ${tmpfile}
}    

make_lesson ./python-obj-system.py
make_lesson ./decorator.py

echo "*** all tutorials generated ***"
