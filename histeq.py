#!/usr/bin/env python

import cv2
import numpy as np

camera = cv2.VideoCapture(0)

def globe(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    return img

def clahe(img):
    img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    return img

while True:
    (grabbed, frame) = camera.read()
    if not grabbed:
        break
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.Canny(frame2, 75, 100)
    cv2.imshow('original', frame2)
    globe2 = globe(frame)
    globe2 = cv2.Canny(globe2, 75, 100)
    cv2.imshow('global', globe2)
    clahe2 = clahe(frame)
    clahe2 = cv2.Canny(clahe2, 75, 100)
    cv2.imshow('clahe', clahe2)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	break

camera.release()
cv2.destroyAllWindows()
