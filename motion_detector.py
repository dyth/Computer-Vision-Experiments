#!/usr/bin/env python

import numpy as np
import imutils
import cv2

camera = cv2.VideoCapture(0)
#camera = cv2.VideoCapture("videos/example_01.mp4")
average = None
n = 1

def detobj(image, frame):
    image = cv2.GaussianBlur(image, (7, 7), 0)     # blur image
    image = cv2.Canny(image, 75, 100)              # edge detection
    image = cv2.dilate(image, None, iterations=20) # dilation
    image = cv2.erode(image, None, iterations=20)  # erosion -- close gaps
    
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1] # find contours

    for (i, c) in enumerate(cnts): # for each contour
        if cv2.contourArea(c) < 100: # ignore small contours FIX THIS
    	    continue
        box = cv2.minAreaRect(c) # rotated bounding box in image
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype = "int")
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2) # draw box
    return frame, image

while True:
    (grabbed, frame) = camera.read()
    if not grabbed: # end of video
	break
    frame = imutils.resize(frame, width = 500)
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # gray
    
    if average is None:
        average = np.float32(grey)
        continue
    cv2.accumulateWeighted(grey, average, 0.25) #1/float(n)) # average
    n = n + 1
    averagecon = cv2.convertScaleAbs(average) # np array -> img
    frameDelta = cv2.absdiff(averagecon, grey)
    frameDelta = cv2.bitwise_and(frameDelta, grey)

    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
        
    cv2.imshow("Object Tracking", detobj(frameDelta, frame)[0])
    cv2.imshow("Object Edges", detobj(frameDelta, frame)[1])
    #cv2.imshow("Average Background", averagecon)
    cv2.imshow("Frame Delta", frameDelta)
    cv2.imshow("Thresh", thresh)
        
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	break

camera.release()
cv2.destroyAllWindows()
