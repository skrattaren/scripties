#!/bin/zsh
mpc --format "%title%\n%artist%\n%album%\n%track%\n%time%" | head -n 5 | grep -v 'volume' > ~/.psi/tune

while [ 1 ]
do
sleep 13s
mpc --format "%title%\n%artist%\n%album%\n%track%\n%time%" | head -n 5 | grep -v 'volume' > ~/.psi/tune
done
