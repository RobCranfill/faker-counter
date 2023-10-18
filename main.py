# faker-counter: a geiger counter simulator.
# Plays WAV files, loud or soft according to the state of a pushbutton.
# robcranfill@gmail.com


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


# Return an audio object for the I2S interface
def get_I2C_audio():
    return audiobusio.I2SOut(bit_clock=board.D9, word_select=board.D10, data=board.D11)

def create_mixer(audio_):
    mixer = audiomixer.Mixer(voice_count=1, channel_count=1,
                             sample_rate=44100, bits_per_sample=16, samples_signed=True)
    audio_.play(mixer)
    return mixer

# start the wav file playing, and wait for it to finish
def play_loaded_wav(mixer_, wav_):
    mixer_.voice[0].play(wav_, loop=False)
    while mixer_.voice[0].playing:
        time.sleep(.1)

def load_wavs(filenames):
    result = []
    for f in filenames:
        try:
            wav = audiocore.WaveFile(open(f, "rb"))
            result.append(wav)
        except Exception as e:
            print(f"Can't find file {f}?")
            raise(e)
    return result


# Our main loop.
# Iterates over the wav files, "low" or "high" according to the button state.
# TODO: play a random wav, rather than the next one?
#
def play_wavs(mixer_, lo_wavs_, hi_wavs_):

    switch = digitalio.DigitalInOut(board.D5)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

    i_lo = 0
    i_hi  = 0
    while True:
        if switch.value: # not pressed - "low" activity
            play_loaded_wav(mixer_, lo_wavs_[i_lo])
            i_lo = (i_lo+1) % len(lo_wavs_)
        else:
            play_loaded_wav(mixer_, hi_wavs_[i_hi])
            i_hi = (i_hi+1) % len(hi_wavs_)


# Hook up to the audio interface
audio = get_I2C_audio()

# new approach
mixer = create_mixer(audio)

lo_wavs = load_wavs(["audio/g1a.wav", "audio/g1b.wav", "audio/g1c.wav"])
hi_wavs = load_wavs(["audio/g2a.wav", "audio/g2b.wav", "audio/g2c.wav"])

play_wavs(mixer, lo_wavs, hi_wavs)

