#!/bin/sh
# A script to set your NowPlayingTune from MPD in Psi
# See http://my.opera.com/Sterkrig/blog/psi-mpd for a little bit
# more detailed description and/or suggestions etc.

# Default MPD settings are (as for mpc) localhost:6600, without password
# To set other values, use environment variables MPD_HOST, MPD_PORT, MPD_PASSWORD
# Either export them, or run script that way:
# $ MPD_HOST="nonlocalhost" MPD_PORT="6666" ./psi_tune.sh

mpc --format "%title%\n%artist%\n%album%\n%track%\n%time%" | head -n -2 > ~/.psi/tune

while [ 1 ]
do
sleep 13s
mpc --format "%title%\n%artist%\n%album%\n%track%\n%time%" | head -n -2 > ~/.psi/tune
done
