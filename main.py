# fc 1

import array
import board
import math
import time
import audiobusio
import audiocore
import audiomixer
import audiopwmio
import digitalio


# must be a PWM-capable pin
OUTPUT_PIN = board.TX


# works for one file!
def play_with_mixer(audio, filename):

    mixer = audiomixer.Mixer(voice_count=1, channel_count=1,
                            sample_rate=44100, bits_per_sample=16, samples_signed=True)
    audio.play(mixer)

    print(f"Playing {filename}...")
    wav = audiocore.WaveFile(open(filename, "rb"))
    mixer.voice[0].play(wav, loop=False)
    s = 0
    while mixer.voice[0].playing:
        # print(f"  waiting #{s}...")
        time.sleep(.1)
        s += 1
    # print(" Done playing!")


def getPWMAudio():
    audio = audiopwmio.PWMAudioOut(OUTPUT_PIN)
    return audio

def getI2CAudio():
    audio = audiobusio.I2SOut(board.D9, board.D10, board.D11)

    return audio

# this works ok
def test_cycle_samples(a):
    while True:
        print("Soft....")
        play_with_mixer(a, "audio/g1a.wav")
        play_with_mixer(a, "audio/g1b.wav")
        play_with_mixer(a, "audio/g1c.wav")
        print("Loud....")
        play_with_mixer(a, "audio/g2a.wav")
        play_with_mixer(a, "audio/g2a.wav")


audio = getI2CAudio()

# works!
# test_cycle_samples(audio)


def test_play_by_button(a):

    quiet_wavs = ["audio/g1a.wav", "audio/g1b.wav", "audio/g1c.wav"]

    switch = digitalio.DigitalInOut(board.D5)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

    i_quiet = 0

    while True:
        if switch.value: # not pressed
            print("NOT pressed")
            play_with_mixer(a, quiet_wavs[i_quiet])
            i_quiet = (i_quiet+1) % 3
        else:
            print("pressed")
            play_with_mixer(a, "audio/g2a.wav")
            play_with_mixer(a, "audio/g2a.wav")
        time.sleep(0.5)

test_play_by_button(audio)


# this is 10 seconds long - too long unless I can interrupt it
# play_with_mixer(audio, "audio/geiger1b.wav")

# these are all too short
# play_with_mixer(audio, "audio/geiger2b.wav")
# play_with_mixer(audio, "audio/geiger3b.wav")
# play_with_mixer(audio, "audio/geiger4b.wav")
# play_with_mixer(audio, "audio/geiger5b.wav")
# play_with_mixer(audio, "audio/geiger6b.wav")

