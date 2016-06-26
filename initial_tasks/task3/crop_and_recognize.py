''''Author: Andy Rosales Elias, EUREKA! 2016, Univeristy of California, Santa Barbara | andy00@umail.ucsb.edu'''

import crop, ocr_contour, os

def run(images_path, training_path):

    for image in os.listdir(images_path):

        # Reads through the images in a directory and crops temperatures
        if not os.path.exists(os.getcwd()+'/temp/'): #if temp folder doesnt exis, create one
            os.makedirs(os.getcwd()+'/temp/')
        crop.crop_image(images_path+image, "temp/right_digit", 1755 + 35, 0, 38, 30) #crops right digit
        crop.crop_image(images_path+image, "temp/left_digit", 1755, 0, 38, 30) #crops left digit
        right = ocr_contour.recognize(os.getcwd()+'/temp/right_digit.jpg', training_path) #recognize right digit
        left = ocr_contour.recognize(os.getcwd()+'/temp/left_digit.jpg', training_path) #recognize left digit
        os.remove(os.getcwd()+'/temp/right_digit.jpg') #clean up temp dir
        os.remove(os.getcwd()+'/temp/left_digit.jpg')
        temperature = left+right
        print "temp is: {0}".format(temperature)

    print "Success."

