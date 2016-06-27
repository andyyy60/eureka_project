import sys
from PIL import Image


def stitch_horizontally(image_list):
    '''Stitches together a list of images for data training purposes'''
    images = map(Image.open, image_list)
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('h_stitch.jpg')

def stitch_vertically(image_list):
    '''Stitches together a list of images for data training purposes, intended to
    be used combined with stitch_horizontally'''
    images = map(Image.open, image_list)
    heights,widths = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (max_height,total_width))

    x_offset =0
    for im in images:
        new_im.paste(im, (0,x_offset))
        x_offset += im.size[1]

    new_im.save('v_stitch.png')