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


OUTPUT_PIN = board.TX # must be PWM-capable pin


def play_wav_pwm(filename, rate):
    wave_file = open(filename, "rb")
    wave = audiocore.WaveFile(wave_file)
    audio = audiopwmio.PWMAudioOut(OUTPUT_PIN)
    print("audio is playing:", audio.playing)
    audio.play(wave)
    time.sleep(4)

def play_laser_pwm():
    wave_file = open("laser20.wav", "rb")
    wave = WaveFile(wave_file)
    audio = AudioOut(OUTPUT_PIN)
    while True:
        print("audio is playing:", audio.playing)
        if not audio.playing:
            audio.play(wave)
            print(f"Playing at {wave.sample_rate * 0.90} %...")
            wave.sample_rate = int(wave.sample_rate * 0.90) # play 10% slower each time
        time.sleep(0.1)

def play_clicks():

    # num_samples = 1000
    # mean = 0
    # std = 1
    # samples = numpy.random.normal(mean, std, size=num_samples)

    length = 8000 // 440
    random_wave_data = array.array("H", [0] * length)
    for i in range(length):
        random_wave_data[i] = int(random.uniform(0, 2**15) + 2 ** 15)

    dac = audiopwmio.PWMAudioOut(OUTPUT_PIN)
    random_wave = audiocore.RawSample(random_wave_data, sample_rate=8000)
    dac.play(random_wave, loop=True)
    time.sleep(1)
    dac.stop()


def play_sine():
    # Generate one period of sine wav.
    length = 8000 // 440
    sine_wave = array.array("H", [0] * length)
    for i in range(length):
        sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)

    dac = audiopwmio.PWMAudioOut(OUTPUT_PIN)
    sine_wave_sample = audiocore.RawSample(sine_wave, sample_rate=8000)
    dac.play(sine_wave_sample, loop=True)
    time.sleep(1)
    dac.stop()


def play_with_mixer(filename):

    audio = audiopwmio.PWMAudioOut(OUTPUT_PIN)
    mixer = audiomixer.Mixer(voice_count=1, channel_count=1, 
                            sample_rate=44100, bits_per_sample=16, samples_signed=True)
    audio.play(mixer)  # attach mixer to audio playback

    print(f"Playing {filename}...")
    wav = audiocore.WaveFile(open(filename, "rb"))
    mixer.voice[0].play(wav, loop=True)
    while True:
        print("doing something else while it plays")
        time.sleep(1)

play_with_mixer("geiger6b.wav")

# play_wav_pwm("laser2.wav", 0)
# play_wav_pwm("geiger3.wav", 0)

# play_laser_pwm()
# play_clicks()
# play_sine()