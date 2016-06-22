#!/usr/bin/python2.7
#todo: edge cases,empty lists
#todo: cleanup with fresh mind

import os, exifread, time

def exif_info2time(ts):
	#changes EXIF date to number of seconds since 1970-01-01
	tpl = time.strptime(ts + 'UTC', '%Y:%m:%d %H:%M:%S%Z')
	return time.mktime(tpl)

#finds images in "sample_images" folder
image_dir = os.getcwd()+"/sample_images/"

timestamp = []
for filename in os.listdir(image_dir):
    f = open(image_dir + filename, 'rb')
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):  # these are not printable
            dt_value = '%s' % tags['Image DateTime']
            timestamp.append(exif_info2time(dt_value))

def assign_clusters(timestamp):
    edge_indexes = []
    for n in range(1, len(timestamp)):
        if((timestamp[n]-timestamp[0])>60):
            edge_indexes.append(n)
    clusters = [[] for i in range(len(edge_indexes))]
    print(len(clusters))
    current_index = 0
    current_cluster = 0
    for elements in range(len(edge_indexes)):
        for times in range(current_index, edge_indexes[elements]):
            clusters[current_cluster].append(timestamp[times])
            current_index = times+1
        current_cluster+=1

    for item in range(len(clusters)):
        for j in (clusters[item]):
            print "Cluster {0}: {1}".format(item, j)


assign_clusters(timestamp)

