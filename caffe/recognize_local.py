import os, csv
list = []
def classify_folder(folder_path):
    '''Recursively transverses through folder classifying
    all files with .JPG/jpg extensions'''
    for item in os.listdir(folder_path):
        local_list = []
        if '.jpg' in str(item).lower(): #if the image is an image
            os.system(
                "python /usr/local/lib/python2.7/dist-packages/tensorflow/models/image/imagenet/classify_image.py --image_file {} > out.txt".format(folder_path+item))
            f = open('out.txt', 'r')
            for line in f:
                local_list.append(line)
            list.append((item,local_list))
        else:
            classify_folder(folder_path+item+'/')
            #print(list)

def write():
    with open('info.csv', 'w') as csvfile:
        fieldnames = ['Image', 'Guess']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow({'Image': item[0], 'Guess': item[1]})


classify_folder("/home/andy/images/")
write()