import pdb
import csv
import math
import numpy as np
from itertools import starmap

raw_data = []


# modified from https://github.com/waddlepon/bigradio/blob/master/bigradio2.py
def play_sine_waves(coes, duration):
    p = pyaudio.PyAudio()
    fs = 44100
    volume = 0.5

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    for c in coes:
        samples = (c[0][0]*np.sin(2*np.pi*np.arange(fs*duration)*c[0][1]/fs) + c[1][0]*np.sin(2*np.pi*np.arange(
            fs*duration)*c[1][1]/fs) + c[2][0]+np.sin(2*np.pi*np.arange(fs*duration)*c[2][1]/fs)).astype(np.float32)
        stream.write(volume*samples)
    stream.stop_stream()
    stream.close()
    p.terminate()


# Code to Generate the data values:
t = np.linspace(0, np.pi, 10001)


def f(x, a):
    s_1 = np.sin(a*2*np.pi*x)+2*np.sin(2*a*2*np.pi*x)+3*np.sin(3*a*2*np.pi*x)
    r_1 = np.sin(10000*2*np.pi*x)
    s_2 = 3*np.sin((a-200)*2*np.pi*x)+2*np.sin(2*(a-200) *
                                               2*np.pi*x)+1*np.sin(3*(a-200)*2*np.pi*x)
    r_2 = np.sin(20000*2*np.pi*x)
    return r_1*s_1 + r_2 * s_2


output1 = np.zeros_like(np.zeros((100, 10001)), dtype='O')
for a in range(0, 100):
    for i in range(0, 10001):
        output1[a, i] = (t[i], 440+a)


output2 = np.zeros_like(np.zeros((10001, 100)), dtype='float')
for i in range(0, 100):
    x = list(starmap(f, output1[i]))
    for j in range(0, 10001):
        output2[j, i] = x[j]

data = output2.transpose().tolist()

# Width of each rectangle in the riemann sum, to approximate the integral
width = math.pi/10000

num = 0
small_total = []
large_total = []
for column in data:
    num += 1
    print("Column: " + str(num))
    small_values = []
    large_values = []
    for b in range(20, 2001):  # cycle through all the octaves, checking their accuracy as the pitches
        # cycle through all of the values in the column (the time interval)
        # Set values to be the stored true value (value * cosine) in order to calculate the integral
        values = []
        # cycle through all of the values in the column, to calculate integral
        for i in range(0, len(column)):
            ft = float(column[i])
            cosine = math.cos((20000+2*b)*math.pi*i*width)
            values.append(ft*cosine)
        # estimate the integral using trapezoids
        integral = np.trapz(values, dx=width)
        if round(integral) != 0:
            small_values.append((integral/(-math.pi/4), b))
    ordered_small = sorted(
        small_values, key=lambda x: abs(round(x[0])-x[0]))[:3]  # Sort the values based on error (distance to integer)
    ordered_large = sorted(
        large_values, key=lambda x: abs(round(x[0])-x[0]))[:3]
    print(ordered_small)
    print(ordered_large)
    small_total.append(ordered_small)
    large_total.append(ordered_large)

play_sine_waves(small_total, 0.1)  # play the sine waves
