#!/bin/sh
mpc --format "%title%\n%artist%\n%album%\n%track%\n%time%" | head -n -2 > ~/.psi/tune

while [ 1 ]
do
sleep 13s
mpc --format "%title%\n%artist%\n%album%\n%track%\n%time%" | head -n -2 > ~/.psi/tune
done
