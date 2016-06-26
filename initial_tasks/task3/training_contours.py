

import sys, imutils
import numpy as np
import cv2

def train(training_image):
    '''trains a kNN model with human input.
    USE: give a training image as an input (look: data folder for examples)
    manually enter the numbers in the boxes to train the model
    if everything goes well, "training complete" messeage should appear'''
    image = cv2.imread(training_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    #################      Now finding Contours         ###################
    # find contours in the thresholded image

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    samples = np.empty((0, 100), np.float32)
    responses = []
    keys = [i for i in range(48, 58)]

    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(image, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        [x, y, w, h] = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)


        roi = thresh[y:y + h, x:x + w]
        roismall = cv2.resize(roi, (10, 10))
        cv2.imshow('norm', image)
        key = cv2.waitKey(0)
        key = 48+(key-1114032) #weird encoding error fix
        print(chr(key))
        if key == chr(27).encode():  # (escape to quit)
            sys.exit()
        elif key in keys:
            responses.append(int(chr(key)))
            sample = roismall.reshape((1, 100))
            samples = np.append(samples, sample, 0)

    responses = np.array(responses, np.float32)
    responses = responses.reshape((responses.size, 1))
    print "training complete"

    samples = np.float32(samples)
    responses = np.float32(responses)

    cv2.imwrite("train_result.png", image)
    np.savetxt('generalsamples.data', samples)
    np.savetxt('generalresponses.data', responses)

