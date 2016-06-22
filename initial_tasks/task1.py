#!/usr/bin/python2.7
import os, exifread


#finds images in "sample_images" folder
image_dir = os.getcwd()+"/sample_images/"

full_path = []
date = []

timestamp = {}
for filename in os.listdir(image_dir):
    f = open(image_dir + filename, 'rb')
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):  # these are not printable
            dt_value = str(tags['Image DateTime']).split()
            timestamp[str(image_dir+filename)] = dt_value


for item in timestamp:
    os.rename(str(item),str("{0}, {1} {2}".format(item, str(timestamp[item][0]).replace(':','-'), timestamp[item][1])))
