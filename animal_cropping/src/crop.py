from PIL import Image
import os

def crop_image(input_image, output_image, start_x, start_y, width, height):
    '''Crops an image given the x,y coordinates as well as width and height. Intended for the use of cropping camera temperatures'''
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    output_img.save(output_image)

def crop_ratio(image, output):
    im = Image.open(image)
    width = im.size[0]
    height = im.size[1]
    crop_image(image, output, 0, 50, width, height-120)


def loop(folder):
    """recursively loops and crops through a directory of images"""
    for image in os.listdir(folder):
        crop_ratio(folder+image, folder+image)
