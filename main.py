# faker-counter: a geiger counter simulator.
# Plays WAV files, loud or soft according to the state of a pushbutton.
# robcranfill@gmail.com
# Version for Raspberry Pi Pico.

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


# defines, so to speak - for Pico
GPIO_PIN_PUSHBUTTON = board.GP13
PIN_GPIO_RED_LED    = board.GP14
PIN_GPIO_GREEN_LED  = board.GP15

PIN_I2S_BCLK = board.GP16
PIN_I2S_LRC  = board.GP17
PIN_I2S_DATA = board.GP18

# The green LED will flash slower than the red, by this factor
GREEN_LED_FLASH_DIVIDER = 4


# create a mixer object to play sounds
def create_mixer():
    audio = audiobusio.I2SOut(bit_clock=PIN_I2S_BCLK, word_select=PIN_I2S_LRC, data=PIN_I2S_DATA)
    mixer = audiomixer.Mixer(voice_count=1, channel_count=1,
                             sample_rate=11025, bits_per_sample=16, samples_signed=True)
    audio.play(mixer)
    return mixer


# load the indicated wav file and return the data
def load_wav(filename):
    try:
        result = audiocore.WaveFile(open(filename, "rb"))
    except Exception as e:
        print(f"Can't load file {filename}")
        raise(e)
    return result


# play one sound continuously until we need to switch.
def play_continuosly(switch_, red_, green_, mixer_, lo_wav, hi_wav):

    wav = lo_wav
    button_was_pressed = False
    led_on = False
    green_counter = 0

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

            led_on = not led_on
            if led_on:
                if button_was_pressed:
                    red_.value = True
                else:
                    green_counter = (green_counter+1) % GREEN_LED_FLASH_DIVIDER
                    if green_counter == 0:
                        green_.value = True
            else:
                red_.value = False
                green_.value = False

            time.sleep(.1)


if __name__ == "__main__":

    # the pushbutton
    switch = digitalio.DigitalInOut(GPIO_PIN_PUSHBUTTON)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

    # the LEDs
    red_led = digitalio.DigitalInOut(PIN_GPIO_RED_LED)
    red_led.direction = digitalio.Direction.OUTPUT

    green_led = digitalio.DigitalInOut(PIN_GPIO_GREEN_LED)
    green_led.direction = digitalio.Direction.OUTPUT

    mixer = create_mixer()

    lo_wav = load_wav("audio/long_lo-b.wav")
    hi_wav = load_wav("audio/long_hi-b.wav")

    play_continuosly(switch, red_led, green_led, mixer, lo_wav, hi_wav)

