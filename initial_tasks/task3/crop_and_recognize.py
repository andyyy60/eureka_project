''''Author: Andy Rosales Elias, EUREKA! 2016, Univeristy of California, Santa Barbara | andy00@umail.ucsb.edu'''

import crop, ocr_contour, os

def run(images_path, training_path):
    '''reads temperature of images in a directory'''
    #TODO: make it only read .JPG and TIFF
    for image in os.listdir(images_path):

        # Reads through the images in a directory and crops temperatures
        if not os.path.exists(os.getcwd()+'/temp/'): #if temp folder doesnt exis, create one
            os.makedirs(os.getcwd()+'/temp/')
        crop.crop_image(images_path+image, "temp/digits", 1710, 0, 115, 30) #crops digits
        temperature = ocr_contour.recognize(os.getcwd()+'/temp/digits.jpg', training_path) #recognize right digit
        os.remove(os.getcwd()+'/temp/digits.jpg') #clean up temp dir
        temp = ''
        for digit in temperature:
            temp += digit
        print "temperature is: {0}".format(temp)

    print "Success."

def run_single(image, training_path):
    """reads temperature for a single image"""
    # Reads through the images in a directory and crops temperatures
    if not os.path.exists(os.getcwd()+'/temp/'): #if temp folder doesnt exis, create one
        os.makedirs(os.getcwd()+'/temp/')
    crop.crop_image(image, "temp/digits", 1710, 0, 115, 30) #crops digits
    temperature = ocr_contour.recognize(os.getcwd()+'/temp/digits.jpg', training_path) #recognize right digit
    os.remove(os.getcwd()+'/temp/digits.jpg') #clean up temp dir
    temp = ''
    for digit in temperature:
        temp += digit
    print "temperature is: {0}".format(temp)

    print "Success."
