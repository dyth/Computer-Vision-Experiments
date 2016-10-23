#!/usr/bin/env python
'''
Find most similar frames between Wombat1.mp4 and wombat.jpg based on akaze matching
'''

import imutils
import cv2
import numpy as np


# return Hamming distance between two frames' keypoints
def kaze_match(im1, im2):
    # detect AKAZE keypoints
    detector = cv2.AKAZE_create()
    gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    kp1, descs1 = detector.detectAndCompute(gray1, None)
    kp2, descs2 = detector.detectAndCompute(gray2, None)    

    # match by Hamming distance and use ratio test to return average distance
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(descs1, descs2, k=2)
    good = []
    distance = 0
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            distance += m.distance + n.distance
            good.append([m])
    return float(distance)/len(good)


# find pair of optimal frames
def findpair(vid1, vid2):
    cap1, cap2 = cv2.VideoCapture(vid1), cv2.VideoCapture(vid2)
    (_, im1), (_, im2) = cap1.read(), cap2.read()
    frame1, opt1, opt2, distance = 0, 0, 0, kaze_match(im1, im2)
    while(cap1.isOpened()):
        frame2 = 0
        while(cap2.isOpened()):
            newdist = kaze_match(im1, im2)
            if (newdist < distance):
                distance, opt1, opt2 = newdist, frame1, frame2
            _, im2 = cap2.read()        
            frame2 += 1
        _, im1 = cap1.read()
        frame1 += 1
    print opt1, opt2


    
# set up images and initialise counter
cap = cv2.VideoCapture('Wombat1.mp4')
im1 = cv2.imread('wombat.jpg')
ret, im2 = cap.read()
frameno, optimal, distance = 0, 0, kaze_match(im1, im2)

# cycle through each image to find optimal pairing
while(cap.isOpened()):
    frameno += 1
    ret, im2 = cap.read()
    newdist = kaze_match(im1, im2)
    if (newdist < distance):
        distance, optimal = newdist, frameno
    if (frameno/10.0 == frameno/10):
        print frameno
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
print optimal

cap = cv2.VideoCapture('Wombat1.mp4')
for i in range(optimal):
    ret, im2 = cap.read()
cv2.imshow("foo", im1)
cv2.imshow("bar", im2)
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
