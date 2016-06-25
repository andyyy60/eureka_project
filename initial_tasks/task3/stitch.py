import sys
from PIL import Image

images = map(Image.open, ['test.png','test.png','test.png','test.png'])
heights,widths = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (max_height,total_width))

x_offset =0
for im in images:
  new_im.paste(im, (0,x_offset))
  x_offset += im.size[1]

new_im.save('no_space_stitch.png')