from PIL import Image
import os

def crop_image(input_image, output_image, start_x, start_y, width, height):
    #temperature is at crop_image("img.JPG","output", 1750, 0, 150, 40)
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    output_img.save(output_image +".JPG")

def gen_grid():

    for image in os.listdir(os.getcwd()+"/train_digits/"):
    # opens an image:
        im = Image.open(os.getcwd()+"/train_digits/"+str(image))
        # creates a new empty image, RGB mode, and size 400 by 400.

        # Iterate through a 4 by 4 grid with 100 spacing, to place my image
        for i in xrange(0, 500, 100):
            for j in xrange(0, 500, 100):
                # I change brightness of the images, just to emphasise they are unique copies.
                new_im = Image.eval(im, lambda x: x + (i + j) / 30)
                # paste the image at location i,j:
                new_im.paste(im, (i, j))

    new_im.save("test.png")





crop_image(os.getcwd() + "/sample_images/Main_2015-01-05_12_34_35_343.JPG", "7", 1755, 0, 38, 30)
#crop_image(os.getcwd()+"/sample_images/Main_2015-01-18_08_52_23_114.JPG","output", 1750, 0, 80, 30) -->  both digits
#crop_image(os.getcwd() + "/sample_images/Main_2015-01-18_08_52_23_114.JPG", "output", 1755, 0, 38, 30) -->  left digit
#crop_image(os.getcwd() + "/sample_images/Main_2015-01-18_08_52_23_114.JPG", "output", 1755 + 35, 0, 38, 30) --> right didit


