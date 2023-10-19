# faker-counter: a geiger counter simulator.
# Plays WAV files, loud or soft according to the state of a pushbutton.
# robcranfill@gmail.com

# std python libs
import board
import random
import time

# adafruit libs
import audiobusio
import audiocore
import audiomixer
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

# load all the indicated wav files and return an array with the data
def load_wavs(filenames):
    result = []
    for f in filenames:
        try:
            wav = audiocore.WaveFile(open(f, "rb"))
            result.append(wav)
        except Exception as e:
            print(f"Can't load file {f}")
            raise(e)
    return result

# start the wav file playing, and wait for it to finish
def play_loaded_wav(mixer_, wav_):
    mixer_.voice[0].play(wav_, loop=False)
    while mixer_.voice[0].playing:
        time.sleep(.1)


# Our main loop.
# Iterates over the wav files, 
# playing a "low" or "high" activity one according to the button state.
#
def play_wavs(mixer_, lo_wavs_, hi_wavs_):

    switch = digitalio.DigitalInOut(board.D5)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

    # it's actually kinda better to play them in sequence, so you never get a repeat :-/
    do_random = False

    i_lo = 0
    i_hi = 0
    while True:
        if switch.value: # not pressed - "low" activity
            if do_random:
                play_loaded_wav(mixer_, random.choice(lo_wavs_))
            else:
                play_loaded_wav(mixer_, lo_wavs_[i_lo])
                i_lo = (i_lo+1) % len(lo_wavs_)
        else:
            if do_random:
                play_loaded_wav(mixer_, random.choice(hi_wavs_))
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
