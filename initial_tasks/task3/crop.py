from PIL import Image
import os

def crop_image(input_image, output_image, start_x, start_y, width, height):
    '''Crops an image given the x,y coordinates as well as width and height. Intended for the use of cropping camera temperatures'''
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    output_img.save(output_image +".jpg")

                                            ##CAMERA 2##
#crop_image(os.getcwd()+"/sample_images/Main_2015-01-18_08_52_23_114.JPG","output", 1750, 0, 80, 30) -->  both digits
#crop_image(os.getcwd() + "/sample_images/Main_2015-01-18_08_52_23_114.JPG", "output", 1755, 0, 38, 30) -->  left digit
#crop_image(os.getcwd() + "/sample_images/Main_2015-01-18_08_52_23_114.JPG", "output", 1755 + 35, 0, 38, 30) --> right didit


