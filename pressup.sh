#!/bin/bash

PRESSUP_INT=
ITERATIONS=

for arg in $@; do
    if [ $arg -gt 20 ]; then
        PRESSUP_INT=$arg
    else
        ITERATIONS=$arg
    fi
done

if [ -z $PRESSUP_INT ]; then
    DOW="$(date +%u)"
    PRESSUP_INT=$(( (($DOW + 1) / 2 + 1) * 30 ))
fi

ITERATIONS="${ITERATIONS:-5}"

echo "Counting for $ITERATIONS sets by $PRESSUP_INT seconde"

countdown () {
    for j in `seq $1 -1 0`; do
        printf " Rest for $j seconds "
        sleep 1
        printf "\r\033[K"
    done
    echo -e '\a'
}

echo "Set #1"
for i in `seq 2 $ITERATIONS`; do
    read -s -r -n1 -p "Press Enter when finished..."
    printf "\r\033[K"
    countdown $PRESSUP_INT
    mpv --msg-level=all=fatal ~/.pressup.snd
    echo "Set #${i}"
done
echo "No need to press everything when finished, just do it (-:E"
