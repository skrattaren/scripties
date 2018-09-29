#!/usr/bin/env bash

# Get currently played song from MPD and run the required tool to calculate and
# write ReplayGain info for the whole album

# Requires:
# - `mpc` to connect to MPD server
# - `vorbisgain` for OGG/Vorbis files
# - `mp3gain` for MP3s
# - `metaflac` for FLAC

OGG_CMD=("vorbisgain" "-a")
MP3_CMD=("mp3gain" "-a")
FLAC_CMD=("metaflac" "--add-replay-gain")

MPD_LIB_DIR="$HOME/musik"

mpd_file=$(mpc current --format="%file%")
cur_file="$MPD_LIB_DIR/$mpd_file"
ext="${cur_file##*.}"
album_dir=$(dirname -- "$cur_file")

case "$ext" in
    "ogg")
        cmd=("${OGG_CMD[@]}")
        ;;
    "mp3")
        cmd=("${MP3_CMD[@]}")
        ;;
    "flac")
        cmd=("${FLAC_CMD[@]}")
        ;;
    *)
        ;;
esac

eval "${cmd[@]}" "\"$album_dir\"/*.$ext"
