#!/usr/bin/env python

from skimage import data, io, segmentation, color
from skimage.future import graph
import cv2

camera = cv2.VideoCapture(0)
(grabbed, cam) = camera.read()

labels1 = segmentation.slic(cam, compactness=30, n_segments=400)
out1 = color.label2rgb(labels1, cam, kind='avg')

def rag(img):
    g = graph.rag_mean_color(img, labels1)
    labels2 = graph.cut_threshold(labels1, g, 29)
    out2 = color.label2rgb(labels2, img, kind='avg')
    return out2

while True:
    (grabbed, cam) = camera.read()
    if not grabbed:    # end of video
        break
    cv2.imshow("Edges2", rag(cam))

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	break

camera.release()
cv2.destroyAllWindows()
