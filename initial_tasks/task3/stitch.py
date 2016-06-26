import sys
from PIL import Image


images = map(Image.open, ['0.JPG','1.JPG','2.JPG','3.JPG','4.JPG','5.JPG','6.JPG','7.JPG','8.JPG','9.JPG'])
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('no_space_stitch.jpg')

################STITCH VERTICALLY######################

# import sys
# from PIL import Image
#
# images = map(Image.open, ['test.png','test.png','test.png','test.png'])
# heights,widths = zip(*(i.size for i in images))
#
# total_width = sum(widths)
# max_height = max(heights)
#
# new_im = Image.new('RGB', (max_height,total_width))
#
# x_offset =0
# for im in images:
#   new_im.paste(im, (0,x_offset))
#   x_offset += im.size[1]
#
# new_im.save('no_space_stitch.png')