# fc 1

# std python libs
import array
import board
import math
import random
import time

# adafruit libs
import audiobusio
import audiocore
import audiomixer
import audiopwmio
import digitalio


import supervisor
supervisor.runtime.autoreload = False  # CirPy 8 and above


# works for one file!
def play_with_mixer(audio, filename):

    mixer = audiomixer.Mixer(voice_count=1, channel_count=1,
                            sample_rate=44100, bits_per_sample=16, samples_signed=True)
    audio.play(mixer)

    # print(f"Playing {filename}...")
    wav = audiocore.WaveFile(open(filename, "rb"))
    mixer.voice[0].play(wav, loop=False)
    s = 0
    while mixer.voice[0].playing:
        # print(f"  waiting #{s}...")
        time.sleep(.1)
        s += 1
    # print(" Done playing!")


def getPWMAudio():
    # must be a PWM-capable pin - not all are
    return audiopwmio.PWMAudioOut(board.TX)

def getI2CAudio():
    return audiobusio.I2SOut(board.D9, board.D10, board.D11)

# this works ok as a test
def test_cycle_samples(a):
    while True:
        print("Low....")
        play_with_mixer(a, "audio/g1a.wav")
        play_with_mixer(a, "audio/g1b.wav")
        play_with_mixer(a, "audio/g1c.wav")
        print("High....")
        play_with_mixer(a, "audio/g2a.wav")
        play_with_mixer(a, "audio/g2a.wav")


# can't go fast enough to sound good
def test_buncha_clicks(a):
    while True:
        play_with_mixer(a, "audio/1click.wav")
        r = random.randrange(0, 100) / 1000
        # print(r)
        time.sleep(r)


def test_play_by_button(a):

    lo_wavs = ["audio/g1a.wav", "audio/g1b.wav", "audio/g1c.wav"]
    hi_wavs = ["audio/g2a.wav", "audio/g2b.wav", "audio/g2c.wav"]

    switch = digitalio.DigitalInOut(board.D5)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

    i_lo = 0
    i_hi  = 0
    while True:
        if switch.value: # not pressed
            play_with_mixer(a, lo_wavs[i_lo])
            i_lo = (i_lo+1) % len(lo_wavs)
        else:
            play_with_mixer(a, hi_wavs[i_hi])
            i_hi = (i_hi+1) % len(hi_wavs)


# Pick an audio interface
# audio = getPWMAudio()
audio = getI2CAudio()

# works!
# test_cycle_samples(audio)

# test_buncha_clicks(audio)

# pretty much it!
test_play_by_button(audio)


# this is 10 seconds long - too long unless I can interrupt it
# play_with_mixer(audio, "audio/geiger1b.wav")

# these are all too short
# play_with_mixer(audio, "audio/geiger2b.wav")
# play_with_mixer(audio, "audio/geiger3b.wav")
# play_with_mixer(audio, "audio/geiger4b.wav")
# play_with_mixer(audio, "audio/geiger5b.wav")
# play_with_mixer(audio, "audio/geiger6b.wav")

