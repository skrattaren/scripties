#!/usr/bin/env zsh

INTERVAL=30

counter=1

FILES=( /opt/homebrew-cask/Caskroom/psi/0.15/Psi.app/Contents/Resources/sound/ft_complete.wav )
FILES[2]=$FILES[1]

while [ true ]; do
    printf "\r\033[K"
    echo -n "Step #$counter..."
    sleep $INTERVAL
    mpv --msg-level=all=fatal ${FILES[@]:0:$(( ($counter + 1) % 2 + 1 ))}
    counter=$((counter+1))
done
