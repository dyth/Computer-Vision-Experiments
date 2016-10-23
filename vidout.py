#!/usr/bin/env python

from imutils.video import VideoStream
import imutils
import cv2

vs = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*"MJPG")
writer = None # video writer

while True:
	grabbed, frame = vs.read()
	if writer is None:
		(h, w) = frame.shape[:2] # image dimensions
		writer = cv2.VideoWriter("foo.avi", fourcc, 20, (w,h), True)

        cv2.imshow("frame", frame)
	writer.write(frame)
        
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
                break

cv2.destroyAllWindows()
vs.release()
writer.release()
