#!/bin/sh
# A script to set your NowPlayingTune from MPD in Psi
# See http://my.opera.com/Sterkrig/blog/psi-mpd for a little bit
# more detailed description and/or suggestions etc.

# Report issues/suggestions here:
# http://code.google.com/p/krigstasks-samling/issues/list

# Default MPD settings are (as for mpc) localhost:6600, without password
# To set other values, use environment variables MPD_HOST, MPD_PORT, MPD_PASSWORD
# Either export them, or run script that way:
# $ MPD_HOST="nonlocalhost" MPD_PORT="6666" ./psi_tune.sh
#
# This version uses 'mpc idle' command for convenience. It requires mpc 0.16 and mpd 0.14
# If you use older versions, see older revisions
#
# 'mpc idle' is known to consume CPU on some systems
# (seems to be fixedfixed in 0.18), so see above

mpc --format "%title%\n%artist%\n%album%\n%track%\n%time%" | head -n -2 > ~/.psi/tune

while [ 1 ]
do

while mpc idle
do
mpc --format "%title%\n%artist%\n%album%\n%track%\n%time%" | head -n -2 > ~/.psi/tune
done

sleep 13
done
