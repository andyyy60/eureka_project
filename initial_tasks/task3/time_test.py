import crop_and_recognize, time, os, chandra_ocr, cv2
import numpy as np


def andy(path, debug = False):
    t1=time.time()
    crop_and_recognize.loop(2, path, debug)
    t2=time.time()
    total =t2-t1
    print total
    f = open('test_results.txt', 'w')
    f.write('Time taken: {}'.format(total))
    f.close()

def chandra(path, debug = False):
    t1=time.time()
    for image in os.listdir(path):
        print chandra_ocr.main(2, str(path+image))
        if debug == True:
            img = cv2.imread(path + image)
            cv2.imshow(image, img)
            key = cv2.waitKey(0)
            print key
            cv2.destroyAllWindows()
    t2=time.time()
    total =t2-t1
    print total
    f = open('test_results.txt', 'w')
    f.write('Time taken: {}'.format(total))

#chandra("/home/andy/images/", True)
#andy("/home/andy/images/", True)

def test():
    im = cv2.imread('/home/andy/ocr_knn/initial_tasks/test.jpg')
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 25, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
    for c in contours:
        if cv2.contourArea(c) > 250:
            [x, y, w, h] = cv2.boundingRect(c)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow("img", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("output.jpg", im)


test()