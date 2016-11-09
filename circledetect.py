import numpy as np
import cv2
import circleTo3D

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
            img = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
            img = cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        return (x,y,radius), img
    return None, img

    # Circle detection: slow and inefficient
    # circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1.2,100,param2=40)

    # if circles is None:
    #     return None, img
    # circle = np.uint16(np.around(circles[0][0]))

    # cv2.circle(img, (circle[0], circle[1]), circle[2], (0,255,0), 4)
    # cv2.rectangle(img, (circle[0]-5, circle[1]-5), (circle[0]+5, circle[1]+5), (0,128,255), -1)
    # return circle, img # is necessary to return converted image

cap = cv2.VideoCapture(0)
cap.set(3, circleTo3D.IMG_WIDTH)
cap.set(4, circleTo3D.IMG_HEIGHT)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.waitKey(2)
while True:
    cap.grab()
    ret, frame = cap.read()

    circle, frame = circle_detect(frame) # frame is edited in this temporary version of the func
    if circle:
        print circleTo3D.circle_to_3D(*circle)
    cv2.imshow('frame',frame)
    c = cv2.waitKey(2)
    if c == 27:
        cv2.destroyWindow('frame')
        cv2.waitKey(2)
        break
