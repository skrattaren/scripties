#!/bin/sh

# Get a fortune from `fortune`, format it, and display via D-Bus notification
# system. Time for quote to hang on the screen is calculated by the word number
# (one second per word)

WHAT="discworld"

fortext="$(fortune $WHAT | fmt -stuw 110)"
length=$(echo "$fortext" | wc -w)
let "time=length*1000"
sw-notify-send "Discworld" "$fortext" -t $time

