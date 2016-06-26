
import cv2
import numpy as np
def recogize(image_path): #todo: make .data files arguments
#######   training part    ###############
    samples = np.loadtxt('/home/andy/PycharmProjects/ocr/generalsamples.data', np.float32)
    responses = np.loadtxt('/home/andy/PycharmProjects/ocr/generalresponses.data', np.float32)
    responses = responses.reshape((responses.size, 1))

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    ############################# testing part  #########################

    im = cv2.imread(image_path)
    out = np.zeros(im.shape, np.uint8)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)


    x, y, w, h = 0, 0, 38, 30


    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
    roi = thresh[y:y + h, x:x + w]
    roismall = cv2.resize(roi, (10, 10))
    roismall = roismall.reshape((1, 100))
    roismall = np.float32(roismall)
    retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
    string = str(int((results[0][0])))

    return int(string)
