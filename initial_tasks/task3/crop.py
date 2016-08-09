from PIL import Image
import os

def crop_image(input_image, output_image, start_x, start_y, width, height):
    '''Crops an image given the x,y coordinates as well as width and height. Intended for the use of cropping camera temperatures'''
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    output_img.save(output_image +".jpg")


def invert(image):
    pic = Image.open(image)
    inverted = Image.eval(pic, lambda (x): 255 - x)
    inverted.save(str(image))





                                            ##CAMERA 3##
#crop_image(os.getcwd() + "/sample_images/BoneH_2015-12-08_06_10_04_7013.JPG", "output", 425, 0, 55, 30)


                                            ##CAMERA 1##
#crop_image(os.getcwd()+"/sample_images/BoneT_2014-06-04_17_56_53_1881.JPG","hunnid", 800, 2350, 100, 95)#<-- 100 F
#crop_image(os.getcwd()+"/sample_images/BoneT_2014-06-05_16_06_03_2009.JPG","outpu", 795 + 35, 2350 + 15, 35, 55)
#crop_image(os.getcwd() + "/sample_images/BoneT_2014-06-05_16_19_08_2016.JPG", "train_digits2/8", 795+35, 2350+15, 35, 55)<--right
#crop_image(os.getcwd()+"/sample_images/BoneT_2014-06-05_09_44_07_1911.JPG","output", 750, 2350, 115, 95)<--both
#crop_image(os.getcwd() + "/sample_images/BoneT_2014-06-05_16_19_08_2016.JPG", "train_digits2/output", 795, 2350+15, 38, 55)<left

                                            ##CAMERA 2##
#crop_image(os.getcwd()+"/sample_images/Main_2015-01-18_08_52_23_114.JPG","output", 1750, 0, 80, 30) -->  both digits
#crop_image(os.getcwd() + "/sample_images/Main_2015-01-18_08_52_23_114.JPG", "output", 1755, 0, 38, 30) -->  left digit
#crop_image(os.getcwd() + "/sample_images/Main_2015-01-18_08_52_23_114.JPG", "output", 1755 + 35, 0, 38, 30) --> right didit


def crop_ratio(image, choice):
    im = Image.open(image)
    width = im.size[0]
    height = im.size[1]
    if choice == 0:
        crop_image(image, "output", 0, 50, width, height-250)


