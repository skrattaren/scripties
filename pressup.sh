#!/bin/bash
if [ -n $1 ]; then
    PRESSUP_INT=$1
fi
if [ -z $PRESSUP_INT ]; then
    DOW="$(date +%u)"
    PRESSUP_INT=$(( (($DOW + 1) / 2 + 1) * 30 ))
fi
countdown () {
    for j in `seq $1 -1 0`; do
        printf " $j "
        sleep 1
        printf "\r\033[K"
    done
    echo
}
echo "Set #1"
for i in {2..8}; do
    read -p "Press Enter when finished..."
    echo "Waiting $PRESSUP_INT seconds..."
    countdown $PRESSUP_INT
    mpv --msglevel=all=fatal /Applications/Psi.app/Contents/Resources/sound/ft_complete.wav
    echo "Set #${i}"
done
echo "No need to press everything when finished, just do it (-:E"
