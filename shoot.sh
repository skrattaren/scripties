#!/bin/sh

SWITCH=''
PATH="${HOME}/bilder/tmp"

if [[ $1 == '-s' ]]
    then SWITCH='-s'
         FILENAME=$2
    else FILENAME=$1
fi

FILE=$PATH/$FILENAME

/usr/bin/scrot $SWITCH $FILE
/usr/bin/optipng $FILE
/usr/bin/uimge -r --usr=#url# $FILE | /usr/bin/xclip

