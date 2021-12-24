#!/usr/bin/env bash

set -e

TOTAL_WORDS=0

make_lesson() {
    local script=$1
    local outfile=$(basename $script .py)".md"
    local tmpfile=$(basename $script .py)".tmp"

    #echo '" Set text width as 72.' >${tmpfile}
    #echo "" >>${tmpfile}
    $script >${tmpfile}
    ./tocgen.py ${tmpfile} ${outfile}
    rm ${tmpfile}

    WORDS=$(wc -w "${outfile}" | awk '{ print $1 }')
    echo "${WORDS} words in ${outfile}"
    ((TOTAL_WORDS+=WORDS))
}    

cat <<EOF
Generating tutorial text:

EOF

make_lesson ./python-obj-system.py
make_lesson ./decorator.py
make_lesson ./gen-iterator.py

cat <<EOF
===
Total number of words: ${TOTAL_WORDS}

*** all tutorials generated ***"
EOF



