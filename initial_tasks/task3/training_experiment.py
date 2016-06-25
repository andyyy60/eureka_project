
import sys
import numpy as np
import cv2

im = cv2.imread('no_space_stitch.png')
im3 = im.copy()

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

#################      Now finding Contours         ###################

image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

samples = np.empty((0, 100), np.float32)
responses = []
keys = [i for i in range(48, 58)]

x,y,w,h = 0, 0, 38, 30

for row in range(4):
    for col in range(10):
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
        roi = thresh[y:y + h, x:x + w]
        roismall = cv2.resize(roi, (10, 10))
        cv2.imshow('norm', im)
        key = cv2.waitKey(0)
        key = 48+(key-1114032)

        if key == chr(27).encode():  # (escape to quit)
            sys.exit()
        elif key in keys:
            responses.append(int(chr(key)))
            sample = roismall.reshape((1, 100))
            samples = np.append(samples, sample, 0)
        x +=38
    x = 0
    w = 38
    y+=30


responses = np.array(responses, np.float32)
responses = responses.reshape((responses.size, 1))
print "training complete"

samples = np.float32(samples)
responses = np.float32(responses)

cv2.imwrite("train_result.png", im)
np.savetxt('generalsamples.data', samples)
np.savetxt('generalresponses.data', responses)
