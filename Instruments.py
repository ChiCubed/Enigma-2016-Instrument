from pyo import *
import numpy as np

notes = np.array([220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00])

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

class ElectricGuitar(object):
    def __init__(self):
        self.noise = SuperSaw(freq=LFO(freq=5, mul=5, add=440, type=7), detune=LFO(freq=6, mul=0.5, add=0.5, type=4), mul=0.6, add=SineLoop(freq=440, mul=0.2, feedback=0.3)).out()

    def play(self, x, y, z):
        self.noise.freq.add = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.add.freq = self.noise.freq.add
        self.noise.mul = 0.6
        self.noise.add.mul = 0.2

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul = 0

    def stop(self):
        self.noise.stop()

class ElectricOrgan(object):
    def __init__(self):
        self.noise = LFO(freq=440, type=7, mul = 0.6, add=SineLoop(freq=880, feedback = 0.1, mul=0.1, add=SineLoop(freq=1760, feedback=0.2, mul=0.1, add=LFO(freq=660, type=3, mul=0.2)))).out()

    def play(self, x, y, z):
        self.noise.freq = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.add.freq = self.noise.freq * 2
        self.noise.add.add.freq = self.noise.freq * 4
        self.noise.add.add.add.freq = self.noise.freq * 1.5
        self.noise.mul = 0.6
        self.noise.add.mul = 0.1
        self.noise.add.add.mul = 0.1
        self.noise.add.add.add.mul = 0.2

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul = 0
        self.noise.add.add.mul = 0
        self.noise.add.add.add.mul = 0

    def stop(self):
        self.noise.stop()

class Synth1(object):
    def __init__(self):
        self.noise = LFO(freq=440, type=3, mul = 0.6, sharp = 0.7, add=LFO(freq=440, type=7, mul=LFO(freq=5, mul=0.6, type=7))).out()

    def play(self, x, y, z):
        self.noise.freq = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.add.freq = self.noise.freq
        self.noise.add.mul.freq = self.noise.freq
        self.noise.mul = 0.6
        self.noise.add.mul.mul = 0.6

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul.mul = 0

    def stop(self):
        self.noise.stop()

class Synth2(object):
    def __init__(self):
        self.noise = LFO(freq=440, type=1, mul=0.6, sharp=0.3, add=LFO(freq=880, mul=LFO(freq=440, mul=0.3, type=7))).out()

    def play(self, x, y, z):
        self.noise.freq = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.mul = 0.6
        self.noise.add.freq = self.noise.freq * 2
        self.noise.add.mul.freq = self.noise.freq
        self.noise.add.mul.mul = 0.3

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul.mul = 0

    def stop(self):
        self.noise.stop()

class Oboe(object):
    def __init__(self):
        self.noise = Sine(freq=440, mul=0.2 * 0.6, phase=0.25, add=Sine(freq=880, mul=0.8 * 0.6, phase=0.25, add=Sine(freq=1320, mul=0.6 * 0.6, phase=0.25, add=Sine(freq=1760, mul=0.23 * 0.6, phase=0.25, add=Sine(freq=4840, mul=0.08 * 0.6, phase=0.25, add=Sine(freq=5280, mul=0.07 * 0.6, phase=0.25)))))).out()

    def play(self, x, y, z):
        self.noise.freq = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.add.freq = self.noise.freq * 2
        self.noise.add.add.freq = self.noise.freq * 3
        self.noise.add.add.add.freq = self.noise.freq * 4
        self.noise.add.add.add.add.freq = self.noise.freq * 11
        self.noise.add.add.add.add.add.freq = self.noise.freq * 12
        self.noise.mul = 0.2 * 0.6
        self.noise.add.mul = 0.8 * 0.6
        self.noise.add.add.mul = 0.6 * 0.6
        self.noise.add.add.add.mul = 0.23 * 0.6
        self.noise.add.add.add.add.mul = 0.08 * 0.6
        self.noise.add.add.add.add.add.mul = 0.07 * 0.6

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul = 0
        self.noise.add.add.mul = 0
        self.noise.add.add.add.mul = 0
        self.noise.add.add.add.add.mul = 0
        self.noise.add.add.add.add.add.mul = 0

    def stop(self):
        self.noise.stop()

class DefaultSine(object):
    def __init__(self):
        self.noise = Sine(freq=440, mul=0.6).out()

    def play(self, x, y, z):
        self.noise.freq = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.mul = 0.6

    def pause(self):
        self.noise.mul = 0

    def stop(self):
        self.noise.stop()
