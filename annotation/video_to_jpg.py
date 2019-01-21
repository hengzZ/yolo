import time
import random
import os
from os import getcwd
from os.path import join

import cv2 as cv

wd = getcwd()
videoname = raw_input("Enter the video name in current directory:\n")
videonamepath = join(wd,videoname)
dirname = join(wd,videoname.split('.')[0])
if not os.path.exists(dirname):
    os.makedirs(dirname)

cap = cv.VideoCapture(videonamepath)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == False:
        print "read frame failed."
        break
    cv.imshow('frame',frame)
    framename = join(dirname,time.strftime("%m%d%H%M%S")+str(random.randint(0,999))+".jpg")
    cv.imwrite(framename,frame)
    
    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()

