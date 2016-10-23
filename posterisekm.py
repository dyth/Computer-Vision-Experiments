#!/usr/bin/env python

from sklearn.cluster import MiniBatchKMeans
import numpy as np
import cv2
import imutils

camera = cv2.VideoCapture(0)
output2 = None

def detobj(image, frame):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.medianBlur(image, 3)
    #image = cv2.GaussianBlur(image, (7, 7), 0)     # blur image
    image = cv2.dilate(image, None, iterations=5) # dilation
    image = cv2.erode(image, None, iterations=5)  # erosion -- close gaps

    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1] # find contours

    for (i, c) in enumerate(cnts): # for each contour
        if cv2.contourArea(c) < 1000: # ignore small contours FIX THIS
    	    continue
        box = cv2.minAreaRect(c) # rotated bounding box in image
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2) # draw box
    return (image, frame)

def posterise(image, clusterno): # imagein # clusterno
    (h, w) = image.shape[:2]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB) #RGB -> L*a*b*
    image = image.reshape((image.shape[0] * image.shape[1], 3)) #image -> vector

    clt = MiniBatchKMeans(clusterno) # k means
    labels = clt.fit_predict(image)
    quant = clt.cluster_centers_.astype("uint8")[labels] # create posterised im

    quant = quant.reshape((h, w, 3)) # vector -> image
    image = image.reshape((h, w, 3))

    quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR) # L*a*b* -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
    return quant

while True:
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=500)
    outputa = posterise(frame, 4)
    outputb = posterise(frame, 2)
    if not grabbed:
        break
    if output2 is None:
        output2 = outputa
        continue
#    difference = cv2.absdiff(outputa, output2)
    cv2.imshow("inonego", outputa)
    cv2.imshow("recursive", outputb)
#    cv2.imshow("Objects", detobj(output, frame)[1])
#    cv2.imshow("Difference", difference)
    output2 = outputa
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	break

camera.release()
cv2.destroyAllWindows()
