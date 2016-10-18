import numpy as np
import cv2
import circleTo3D

def circle_detect(img):    
    cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,5,100,param2=40)

    circle = np.uint16(np.around(circles[0][0]))
    cv2.circle(img, (circle[0], circle[1]), circle[2], (0,255,0), 4)
    cv2.rectangle(img, (circle[0]-5, circle[1]-5), (circle[0]+5, circle[1]+5), (0,128,255), -1)
    return circle #, img is necessary to return converted image

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.waitKey(30)
while True:
    ret, frame = cap.read()

    circle = circle_detect(frame) # frame is edited in this temporary version of the func
    cv2.imshow('frame',frame)
    cv2.waitKey(30)
