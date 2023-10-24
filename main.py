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

# turn off auto-reload - that messes with the audio
import supervisor
supervisor.runtime.autoreload = False  # CirPy 8 and above

# defines, so to speak
PIN_PUSHBUTTON = board. D5 # was D6, but I moved it farther from I2S line
PIN_I2S_BCLK   = board. D9
PIN_I2S_LRC    = board.D10
PIN_I2S_DATA   = board.D11


def create_mixer():
    audio = audiobusio.I2SOut(bit_clock=PIN_I2S_BCLK, word_select=PIN_I2S_LRC, data=PIN_I2S_DATA)
    mixer = audiomixer.Mixer(voice_count=1, channel_count=1,
                             sample_rate=44100, bits_per_sample=16, samples_signed=True)
    audio.play(mixer)
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
def play_in_sequence(switch_, mixer_, lo_wavs_, hi_wavs_):

    # it's actually kinda better to play them in sequence, so you never get a repeat :-/
    do_random = False

    i_lo = 0
    i_hi = 0
    while True:
        if switch_.value: # not pressed - "low" activity
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


# play one sound continuously until we need to switch!
def play_continuosly(switch_, mixer_, lo_wav, hi_wav):

    wav = lo_wav
    button_was_pressed = False

    while True:

        mixer_.voice[0].play(wav, loop=True)

        while mixer_.voice[0].playing:
            if not button_was_pressed and not switch_.value: # button pressed
                wav = hi_wav
                button_was_pressed = True
                break
            elif button_was_pressed and switch_.value: # button not pressed
                wav = lo_wav
                button_was_pressed = False
                break
            time.sleep(.1)


# Play the files one after the other, switching as needed
def method_1(switch_):

    mixer = create_mixer()

    lo_wavs = load_wavs(["audio/g1a.wav", "audio/g1b.wav", "audio/g1c.wav"])
    hi_wavs = load_wavs(["audio/g2a.wav", "audio/g2b.wav", "audio/g2c.wav"])

    play_in_sequence(switch_, mixer, lo_wavs, hi_wavs)


# play the low or high file continuously until we need to switch
def method_2(switch_):

    mixer = create_mixer()

    lo_wav = load_wavs(["audio/long_lo.wav"])[0]
    hi_wav = load_wavs(["audio/long_hi.wav"])[0]

    play_continuosly(switch_, mixer, lo_wav, hi_wav)


# the pushbutton
switch = digitalio.DigitalInOut(PIN_PUSHBUTTON)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# method_1(switch)
method_2(switch)
