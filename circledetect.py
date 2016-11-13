import numpy as np
import cv2
import circleTo3D
import timeit
import os

from pyo import *

import Instruments

# #########################################################
# ## Based on https://gist.github.com/THeK3nger/3624478/ ##
# #########################################################
#
# import os
# import wave
# import threading
# import sys
#
# from scipy import signal
#
# # PyAudio Library
# import pyaudio
#
# class FrequencyLoop(threading.Thread) :
#   """
#   A simple class based on PyAudio to play wave loop.
#   It's a threading class. You can play audio while your application
#   continues to do its stuff. :)
#   """
#
#   def __init__(self,frequency,volume=1.0) :
#     """
#     Initialize `FrequencyLoop` class.
#     PARAM:
#         -- filepath (String) : File Path to wave file.
#         -- loop (boolean)    : True if you want loop playback.
#                                False otherwise.
#     """
#     super(FrequencyLoop, self).__init__()
#     self.frequency = frequency
#     self.loop = True
#     self.volume = volume
#
#   def run(self):
#     # Open Wave File and start play!
#     player = pyaudio.PyAudio()
#
#     # Open Output Stream (basen on PyAudio tutorial)
#     stream = player.open(format = pyaudio.paFloat32,
#         channels = 1,
#         rate = 44100,
#         output = True)
#
#     # PLAYBACK LOOP
#     # Prevent frequency from changing mid-sound
#     while self.loop:
#         freq = self.frequency
#         if freq >= 10:
#             duration = 1.0 / freq
#             samples = signal.sawtooth(2*np.pi*np.arange(44100*duration)*freq/44100, 0.5).astype(np.float32)
#             stream.write(samples * self.volume)
#     stream.stop_stream()
#     stream.close()
#
#     player.terminate()
#
#   def play(self) :
#     """
#     Just another name for self.start()
#     """
#     self.start()
#
#   def stop(self) :
#     """
#     Stop playback.
#     """
#     self.loop = False
#
# ######
# ######

def circle_detect(img):
    # cimg = cv2.medianBlur(img, 3)
    cimg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    mask = np.zeros((cimg.shape[0], cimg.shape[1], 1), np.uint8)
    # HOME: cv2.inRange(cimg, np.array([160,200,70]), np.array([185,255,210]), mask)
    cv2.inRange(cimg, np.array([145,140,40]), np.array([190,255,255]), mask)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # mask = cv2.GaussianBlur(mask, (9,9), 2)

    # img = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    # img = cv2.bitwise_and(img,img,mask=mask)

    # PyImageSearch Ball Tracking
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(contours):
        c = max(contours, key=cv2.contourArea)
        # centroid = np.uint16(np.around([m["m10"]/m["m00"],m["m01"]/m["m00"]]))
        # print centroid

        # m = cv2.moments(c)
        # center = (int(m["m10"]/m["m00"]), int(m["m01"]/m["m00"]))

        ((x,y),radius) = cv2.minEnclosingCircle(c)

        if radius > 5: # for example
            # img = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
            img = cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            return (x,y,radius), img

    # Circle detection: slow and inefficient
    # circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1.2,100,param2=40)

    # if circles is None:
    #     return None, img
    # circle = np.uint16(np.around(circles[0][0]))

    # cv2.circle(img, (circle[0], circle[1]), circle[2], (0,255,0), 4)
    # cv2.rectangle(img, (circle[0]-5, circle[1]-5), (circle[0]+5, circle[1]+5), (0,128,255), -1)
    # return circle, img # is necessary to return converted image

    return None, img

cap = cv2.VideoCapture(0)
cap.set(3, circleTo3D.IMG_WIDTH)
cap.set(4, circleTo3D.IMG_HEIGHT)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.waitKey(2)
lastpos = None
lasttime = timeit.default_timer() # cap.get(cv2.CAP_PROP_POS_MSEC) not working

# noise = FrequencyLoop(0, 0.5)
# noise.play()
s = Server(nchnls=2, duplex=0, audio='portaudio').boot()
s.start()

instrument = Instruments.ElectricGuitar(play=False)
# lfo = Sine(.5, phase=[0,.5], mul=.5, add=.5)
# modulator = Instruments.RingMod(instrument.noise, freq=[220,1760], mul=lfo).out()
dualiser = Pan(instrument.noise).out()

i = 0
while os.path.isfile(os.path.expanduser('~') + "/Desktop/recording" + str(i) + ".wav"):
    i += 1
rec = Record(dualiser, filename=os.path.expanduser('~') + "/Desktop/recording" + str(i) + ".wav")

while True:
    cap.grab()
    ret, frame = cap.read()

    circle, frame = circle_detect(frame) # frame is edited in this temporary version of the function
    if circle:
        pos = circleTo3D.circle_to_3D(*circle)
        time = timeit.default_timer() # cap.get(cv2.CAP_PROP_POS_MSEC)
        dt = time - lasttime
        if lastpos is not None and dt > 0:
            velocity = map(lambda x, y: (x - y)/dt, pos, lastpos)

        # This is suited to being able to play any note.
        # noise.setFreq(abs(pos[0]+4)*30+100)
        # We want to 'snap' notes

        instrument.play(*pos)
        # modulator.freq = [instrument.mainFreq()*0.5, instrument.mainFreq() * 1.5]

        lastpos = pos
        lasttime = time
    else:
        # noise.frequency = 0 # Don't play
        instrument.pause()

    cv2.imshow('frame',frame)
    c = cv2.waitKey(2)
    if c == 27:
        cv2.destroyWindow('frame')
        cv2.waitKey(2)
        instrument.stop()
        rec.stop()
        s.stop()

        print "\n\n\n\n\n#############################"
        print "To listen to your recording, please navigate to " + os.path.expanduser('~') + "/Desktop and enter the following command:"
        print "omxplayer --vol -2000 recording" + str(i) + ".wav"
        print "#############################\n\n\n\n\n"
        # manual kill
        os.system('kill %d ' % os.getpid())
        break
