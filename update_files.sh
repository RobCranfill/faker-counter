#!/bin/bash
# copy only the needed files over

CP_LOC=/media/rob/CIRCUITPY/

cp main.py $CP_LOC/

mkdir $CP_LOC/audio
cp audio/long_hi.wav $CP_LOC/audio
cp audio/long_lo.wav $CP_LOC/audio

