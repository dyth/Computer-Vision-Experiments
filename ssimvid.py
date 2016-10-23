#!/usr/bin/env python

from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

cap = cv2.VideoCapture('Wombat1.mp4')

def mse(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err # return sum of squared difference between image

def compare_images(imageA, imageB):
	m = mse(imageA, imageB)  # mean squared error
	s = ssim(imageA, imageB) # structural similarity
        vis = np.concatenate((imageA, imageB), axis=1)
        #print "MSE: %.2f, SSIM: %.2f" % (m, s)
        #cv2.imshow("comparison", vis)
        return s

im1 = cv2.imread("wombat.jpg")
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY) # im -> greyscale

previous = 0
while(cap.isOpened()):
        ret, im2 = cap.read()
        im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        if (im1.shape[0]*im1.shape[1] > im2.shape[0]*im2.shape[1]):
                im1 = cv2.resize(im1, (im2.shape[1], im2.shape[0]))
        else:
                im2 = cv2.resize(im2, (im1.shape[1], im1.shape[0]))
        score = compare_images(im1, im2) # compare the images
        if (score > previous):
                frag = im2
                previous = score
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #        break

cv2.imshow("frag", frag)
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
