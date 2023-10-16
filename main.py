# fc 1

import array
import board
import math
import time
# from audiocore import WaveFile
# from audiopwmio import PWMAudioOut as AudioOut
import audiocore
import audiomixer
import audiopwmio
import ulab.numpy as numpy
import random


# must be a PWM-capable pin
OUTPUT_PIN = board.TX 


# works for one file!
def play_with_mixer(filename):

    audio = audiopwmio.PWMAudioOut(OUTPUT_PIN)
    mixer = audiomixer.Mixer(voice_count=1, channel_count=1, 
                            sample_rate=44100, bits_per_sample=16, samples_signed=True)
    audio.play(mixer)

    print(f"Playing {filename}...")
    wav = audiocore.WaveFile(open(filename, "rb"))
    mixer.voice[0].play(wav, loop=False)
    s = 0
    while mixer.voice[0].playing:
        print(f"doing something else while it plays #{s}...")
        time.sleep(1)
        s += 1
    print("Done playing!")


play_with_mixer("audio/geiger1b.wav")

