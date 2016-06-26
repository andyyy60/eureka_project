''''Author: Andy Rosales Elias, EUREKA! 2016, Univeristy of California, Santa Barbara | andy00@umail.ucsb.edu'''

import crop, ocr_contour, os, chandra_ocr

def run():
    directory = os.getcwd()+'/sample_images/'

    for image in os.listdir(directory):

        # Reads through the images in a directory and crops temperatures
        crop.crop_image(directory+image, "temp/right_digit", 1755 + 35, 0, 38, 30) #crops right digit
        crop.crop_image(directory+image, "temp/left_digit", 1755, 0, 38, 30) #crops left digit
        right = ocr_contour.recognize(os.getcwd()+'/temp/right_digit.jpg')
        left = ocr_contour.recognize(os.getcwd()+'/temp/left_digit.jpg')
        chandra = chandra_ocr.main(2, directory+image)
        os.remove(os.getcwd()+'/temp/right_digit.jpg')
        os.remove(os.getcwd()+'/temp/left_digit.jpg')
        temperature = left+right
        if str(temperature) not in chandra:
            print "mismatch: {0} {1} {2}".format(temperature, chandra, image)


run()
