#!/usr/bin/env zsh

INTERVAL=30

if [ ! -n "$1" ]; then
    echo "Need a file argument to beep with" > /dev/stderr
    exit 1
fi

counter=1

FILES=( "$1" )
FILES[2]=$FILES[1]

while [ true ]; do
    printf "\r\033[K"
    echo -n "Step #$counter..."
    sleep $INTERVAL
    mpv --msg-level=all=fatal ${FILES[@]:0:$(( ($counter + 1) % 2 + 1 ))}
    counter=$((counter+1))
done
