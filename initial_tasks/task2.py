#!/usr/bin/python2.7
#todo: edge cases,empty lists
#todo: cleanup with fresh mind
#TODO: ADD LOOP THAT RENAMES FILES TEMPORARY TO AVOID CONFLICTS

import os, exifread, time, operator

def exif_info2time(ts):
	#changes EXIF date to number of seconds since epoch
	tpl = time.strptime(ts + 'UTC', '%Y:%m:%d %H:%M:%S%Z')
	return time.mktime(tpl)

#finds images in "sample_images" folder
image_dir = os.getcwd()+"/sample_images/"


timestamp = {}
filename_stamp = {}
for filename in os.listdir(image_dir):
    f = open(image_dir + filename, 'rb')
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):  # these are not printable
            dt_sec = '%s' % tags['Image DateTime']
            timestamp[str(filename)] = exif_info2time(dt_sec)
            dt_value = str(tags['Image DateTime']).split()
            filename_stamp[str(filename)] = dt_value







sorted_timestamps = sorted(timestamp.items(), key=operator.itemgetter(1)) # create sorted list of (filename, time) tuples



def assign_clusters(timestamps):
    edge_indexes = []
    current = 0;
    for n in range(1, len(sorted_timestamps)):
        if(abs(sorted_timestamps[n][1]-sorted_timestamps[current][1])>60):
            edge_indexes.append(n)
            current = n
    clusters = [[] for i in range(len(edge_indexes)+1)]
    current_index = 0
    current_cluster = 0
    for elements in range(len(edge_indexes)):
        for times in range(current_index, edge_indexes[elements]):
            clusters[current_cluster].append(sorted_timestamps[times][1])
            current_index = times+1
        current_cluster+=1

    for i in range(current_index, len(sorted_timestamps)):
        clusters[current_cluster].append(sorted_timestamps[i][1])
    return clusters


print assign_clusters(timestamp)
def cluster_id(time_in_seconds, cluster):
    #returns sequence id of cluster given filename
    for sequence in range(len(cluster)):
        for time in cluster[sequence]:
            if time_in_seconds == time:
                return sequence



for item in sorted_timestamps:
    os.rename(str(image_dir+item[0]),str("{0}_{1}_{2}_{3}.JPG".format(image_dir+item[0][:-4], str(filename_stamp[item[0]][0]).replace(':','-'), str(filename_stamp[item[0]][1]), str(cluster_id(item[1], assign_clusters(timestamp))))))
