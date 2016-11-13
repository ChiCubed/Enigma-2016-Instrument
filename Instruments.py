from pyo import *
import numpy as np

notes = np.array([220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00])

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

# From the Pyo tutorial
class RingMod(PyoObject):
    """
    Ring modulator.

    Ring modulation is a signal-processing effect in electronics
    performed by multiplying two signals, where one is typically
    a sine-wave or another simple waveform.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        freq : float or PyoObject, optional
            Frequency, in cycles per second, of the modulator.
            Defaults to 100.

    >>> s = Server().boot()
    >>> s.start()
    >>> src = SfPlayer(SNDS_PATH+"/transparent.aif", loop=True, mul=.3)
    >>> lfo = Sine(.25, phase=[0,.5], mul=.5, add=.5)
    >>> ring = RingMod(src, freq=[800,1000], mul=lfo).out()

    """

    def __init__(self, input, freq=100, mul=1, add=0):
        PyoObject.__init__(self, mul, add)

        self._input = input
        self._freq = freq

        self._in_fader = InputFader(input)

        in_fader, freq, mul, add, lmax = convertArgsToLists(self._in_fader, freq, mul, add)

        self._mod = Sine(freq=freq, mul=in_fader)
        self._ring = Sig(self._mod, mul=mul, add=add)
        self._base_objs = self._ring.getBaseObjects()

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.

        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setFreq(self, x):
        """
        Replace the `freq` attribute.

        :Args:

            x : float or PyoObject
                New `freq` attribute.

        """
        self._freq = x
        self._mod.freq = x

    @property
    def input(self):
        """PyoObject. Input signal to process."""
        return self._input
    @input.setter
    def input(self, x):
        self.setInput(x)

    @property
    def freq(self):
        """float or PyoObject. Frequency of the modulator."""
        return self._freq
    @freq.setter
    def freq(self, x):
        self.setFreq(x)

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(10, 2000, "log", "freq", self._freq),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    def play(self, dur=0, delay=0):
        self._mod.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self):
        self._mod.stop()
        return PyoObject.stop(self)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self._mod.play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)

class ElectricGuitar(object):
    def __init__(self, play=True):
        self.noise = SuperSaw(freq=LFO(freq=5, mul=5, add=440, type=7), detune=LFO(freq=6, mul=0.5, add=0.5, type=4), mul=0.6, add=SineLoop(freq=440, mul=0.2, feedback=0.3))
        if play:
            self.noise.out()

    def play(self, x, y, z):
        self.noise.freq.add = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.add.freq = self.noise.freq.add
        self.noise.mul = 0.6
        self.noise.add.mul = 0.2

    def mainFreq(self):
        return self.noise.freq.add

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul = 0

    def stop(self):
        self.noise.stop()

class ElectricOrgan(object):
    def __init__(self, play=True):
        self.noise = LFO(freq=440, type=7, mul = 0.6, add=SineLoop(freq=880, feedback = 0.1, mul=0.1, add=SineLoop(freq=1760, feedback=0.2, mul=0.1, add=LFO(freq=660, type=3, mul=0.2))))
        if play:
            self.noise.out()

    def play(self, x, y, z):
        self.noise.freq = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.add.freq = self.noise.freq * 2
        self.noise.add.add.freq = self.noise.freq * 4
        self.noise.add.add.add.freq = self.noise.freq * 1.5
        self.noise.mul = 0.6
        self.noise.add.mul = 0.1
        self.noise.add.add.mul = 0.1
        self.noise.add.add.add.mul = 0.2

    def mainFreq(self):
        return self.noise.freq

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul = 0
        self.noise.add.add.mul = 0
        self.noise.add.add.add.mul = 0

    def stop(self):
        self.noise.stop()

class Synth1(object):
    def __init__(self, play=True):
        self.noise = LFO(freq=440, type=3, mul = 0.6, sharp = 0.7, add=LFO(freq=440, type=7, mul=LFO(freq=5, mul=0.6, type=7)))
        if play:
            self.noise.out()

    def play(self, x, y, z):
        self.noise.freq = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.add.freq = self.noise.freq
        self.noise.add.mul.freq = self.noise.freq
        self.noise.mul = 0.6
        self.noise.add.mul.mul = 0.6

    def mainFreq(self):
        return self.noise.freq

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul.mul = 0

    def stop(self):
        self.noise.stop()

class Synth2(object):
    def __init__(self, play=True):
        self.noise = LFO(freq=440, type=1, mul=0.6, sharp=0.3, add=LFO(freq=880, mul=LFO(freq=440, mul=0.3, type=7)))
        if play:
            self.noise.out()

    def play(self, x, y, z):
        self.noise.freq = float(find_nearest(notes, abs(x+1)*100+200))
        self.noise.mul = 0.6
        self.noise.add.freq = self.noise.freq * 2
        self.noise.add.mul.freq = self.noise.freq
        self.noise.add.mul.mul = 0.3

    def mainFreq(self):
        return self.noise.freq

    def pause(self):
        self.noise.mul = 0
        self.noise.add.mul.mul = 0

    def stop(self):
        self.noise.stop()

class Oboe(object):
    def __init__(self, play=True):
        self.noise = Sine(freq=440, mul=0.2 * 0.6, phase=0.25, add=Sine(freq=880, mul=0.8 * 0.6, phase=0.25, add=Sine(freq=1320, mul=0.6 * 0.6, phase=0.25, add=Sine(freq=1760, mul=0.23 * 0.6, phase=0.25, add=Sine(freq=4840, mul=0.08 * 0.6, phase=0.25, add=Sine(freq=5280, mul=0.07 * 0.6, phase=0.25))))))
        if play:
            self.noise.out()

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

    def mainFreq(self):
        return self.noise.freq

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

    def mainFreq(self):
        return self.noise.freq

    def pause(self):
        self.noise.mul = 0

    def stop(self):
        self.noise.stop()
