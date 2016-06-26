''''Author: Andy Rosales Elias, EUREKA! 2016, Univeristy of California, Santa Barbara | andy00@umail.ucsb.edu'''

import crop, ocr_experiment, os, chandra_ocr

def run():
    directory = os.getcwd()+'/sample_images/'

    for image in os.listdir(directory):

        # Reads through the images in a directory and crops temperatures
        crop.crop_image(directory+image, "temp/right_digit", 1755 + 35, 0, 38, 30) #crops right digit
        crop.crop_image(directory+image, "temp/left_digit", 1755, 0, 38, 30) #crops left digit
        right = ocr_experiment.recogize(os.getcwd()+'/temp/right_digit.jpg')
        left = ocr_experiment.recogize(os.getcwd()+'/temp/left_digit.jpg')
        os.remove(os.getcwd()+'/temp/right_digit.jpg')
        os.remove(os.getcwd()+'/temp/left_digit.jpg')
        temperature = left*10+right
        print "The temperature is {0}".format(temperature), image


run()
