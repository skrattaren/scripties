#!/bin/bash

# This script is intended to be a helper for those who follow famous
# "One hundred pushups" fitness program: http://www.hundredpushups.com/
# (or similar ones).

### What does it do?
# Basically script just notifies you when it's time to start a new set of
# exercises with sound and terminal bell.  Default settings are 5 sets with
# number of seconds to rest in between determined automagically depending on
# day of the week (Mon and Tue -- 60 sec, Wed and Thu -- 90 sec, Fri and Sat --
# 120 sec), which matches the first 4 weeks of OHP program.  Of course, it's
# possible to override those, and script is a bit heuristic: if you pass it an
# argument, it assumes that number less than 21 must be number of sets, and
# number greater is probably a rest interval. So (examples run on Friday):

#  % ./pressup.sh
# Counting for 5 sets by 120 seconds
#
#  % ./pressup.sh 8
# Counting for 8 sets by 120 seconds
#
#  % ./pressup.sh 8 45
# Counting for 8 sets by 45 seconds
#
#  % ./pressup.sh 45 8
# Counting for 8 sets by 45 seconds
#
#  % ./pressup.sh 45
# Counting for 5 sets by 45 seconds

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the `GNU General Public License`_ for details.
#
# .. GNU General Public License: http://www.gnu.org/licenses/
# (c) 2014-2015, Николай Шуйский (Nikolaj Sjujskij) <skrattaren@yandex.ru>


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

echo "Counting for $ITERATIONS sets by $PRESSUP_INT seconds"

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
echo "No need to press anything when finished, just do it (-:E"
