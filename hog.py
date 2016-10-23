#!/usr/bin/env python

import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import data, color, exposure

import cv2

camera = cv2.VideoCapture(0)
#camera = cv2.VideoCapture('wombat1.mp4')

def hogg(image):
    image = color.rgb2gray(image)
    fd, hog_image = hog(image, orientations=6, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualise=True)
    hog_image_rescaled = exposure.rescale_intensity(hog_image,in_range=(0,0.02))
    cv2.imshow("Hogwarts", hog_image_rescaled)

while(camera.isOpened()):
    (grabbed, frame) = camera.read()
    hogg(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
