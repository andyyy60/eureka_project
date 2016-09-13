
import cv2, imutils
import numpy as np

def recognize(images_path, training_path, pass_info = False):
    if "camera_1" in training_path:
        threshhold =75
        area = 110
    elif "camera_2" in training_path:
        threshhold =151
        area = 70
    elif "camera_3" in training_path:
        threshhold = 151
        area = 70
    #######   training part    ###############
    samples = np.loadtxt(training_path+'generalsamples.data', np.float32)
    responses = np.loadtxt(training_path+'generalresponses.data', np.float32)
    responses = responses.reshape((responses.size, 1))

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    ############################# testing part  #########################

    image = cv2.imread(images_path)
    out = np.zeros(image.shape, np.uint8)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, threshhold, 255, cv2.THRESH_BINARY)[1]#dont change 151

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # new = cv2.drawContours(image, cnts, -1, (0, 255, 0), 3)
    # cv2.imshow('im', new)
    # cv2.imshow('out', out)
    # cv2.waitKey(0)
    content = []
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        [x, y, w, h] = cv2.boundingRect(c)
        if cv2.contourArea(c)>area: #the higher the threshold, the smaller the area
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = thresh[y:y + h, x:x + w]
            roismall = cv2.resize(roi, (10, 10))
            roismall = roismall.reshape((1, 100))
            roismall = np.float32(roismall)
            retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
            string = str(int((results[0][0])))
            if pass_info: #returns temp between C and F symbols (camera 1)
                content.append((string, [cX,cY]))
            else:
                if string != str(42):
                    cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))
                    content.append(string)
    content.reverse()
    return content
