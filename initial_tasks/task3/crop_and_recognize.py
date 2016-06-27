''''Author: Andy Rosales Elias, EUREKA! 2016, Univeristy of California, Santa Barbara | andy00@umail.ucsb.edu'''

import crop, ocr_contour, os, chandra_ocr

def run(image, training_path):
    '''reads temperature of images in a directory'''
    #TODO: make it only read .JPG and TIFF
    #TODO: Make second argument 1,2,3
    if not os.path.exists(os.getcwd()+'/temp/'): #if temp folder doesnt exis, create one
        os.makedirs(os.getcwd()+'/temp/')
    crop.crop_image(image, "temp/digits", 1710, 0, 115, 30) #crops digits
    temperature = ocr_contour.recognize(os.getcwd()+'/temp/digits.jpg', training_path) #recognize right digit
    os.remove(os.getcwd()+'/temp/digits.jpg') #clean up temp dir
    temp = ''
    for digit in temperature:
        temp += digit
    print "temperature is: {0}".format(temp)



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

def run2(image, training_path):
    '''reads temperature of images in a directory. CAMERA 1 ONLY'''
    #TODO: Make second argument 1,2,3
    #TODO: MAKE NEGATIVE SIGN VALUE MEAN SOMETHING(currently means 45)
    if not os.path.exists(os.getcwd() + '/temp/'):  # if temp folder doesnt exis, create one
        os.makedirs(os.getcwd() + '/temp/')
    crop.crop_image(image,'temp/digits',  800, 2350, 100, 95)
    crop.invert(os.getcwd() + '/temp/digits.jpg')
    digits = len(ocr_contour.recognize(os.getcwd() + '/temp/digits.jpg', training_path))
    temperature = ''
    if digits == 1:  # crop rightmost digit
        crop.crop_image(image, "temp/1", 795 + 35, 2350 + 15, 35, 55)
        crop.invert(os.getcwd() + '/temp/1.jpg')
        temperature = ocr_contour.recognize(os.getcwd() + '/temp/1.jpg', training_path)
        os.remove(os.getcwd() + '/temp/1.jpg')  # clean up temp dir
    if digits == 2:
        crop.crop_image(image, "temp/1", 795 + 35, 2350 + 15, 35, 55)
        crop.crop_image(image, "temp/2", 795, 2350 + 15, 38, 55)
        crop.invert(os.getcwd() + '/temp/1.jpg')
        crop.invert(os.getcwd() + '/temp/2.jpg')
        right = ocr_contour.recognize(os.getcwd() + '/temp/1.jpg', training_path)
        left = ocr_contour.recognize(os.getcwd() + '/temp/2.jpg', training_path)
        temperature = left[0] + right[0]
        os.remove(os.getcwd() + '/temp/1.jpg')  # clean up temp dir
        os.remove(os.getcwd() + '/temp/2.jpg')  # clean up temp dir
    elif digits == 3:
        crop.crop_image(image, "temp/1", 795 + 35, 2350 + 15, 35, 55)
        crop.crop_image(image, "temp/2", 795, 2350 + 15, 38, 55)
        crop.crop_image(image, "temp/3", 800+64, 2365, 100-57, 55)
        crop.invert(os.getcwd() + '/temp/1.jpg')
        crop.invert(os.getcwd() + '/temp/2.jpg')
        crop.invert(os.getcwd() + '/temp/3.jpg')
        right = ocr_contour.recognize(os.getcwd() + '/temp/1.jpg', training_path)
        left = ocr_contour.recognize(os.getcwd() + '/temp/2.jpg', training_path)
        extra = ocr_contour.recognize(os.getcwd() + '/temp/3.jpg', training_path)
        temperature = left[0]+extra[0] + right[0]
    print "temperature is: {0}".format(temperature), image


