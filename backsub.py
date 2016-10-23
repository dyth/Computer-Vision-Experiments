#!/usr/bin/env python
'''
Background subtraction using default cv2 functions
'''

import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while(True):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame) 
    cv2.imshow("frame", fgmask)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
