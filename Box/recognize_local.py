import os, csv
list = []
def classify_folder(folder_path):
    '''Recursively transverses through folder classifying
    all files with .JPG/jpg extensions'''
    for item in os.listdir(folder_path):
        if '.jpg' in str(item).lower(): #if the image is an image
            os.system('python classify.py {} foo > out.txt'.format(folder_path+item))#call classify.py and output to out.txt
            f = open('out.txt', 'r')
            temp = f.readlines()[4]
            list.append((item,temp))
        else:
            classify_folder(folder_path+item+'/')
    print(list)

def write():
    with open('info.csv', 'w') as csvfile:
        fieldnames = ['Image', 'Guess']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow({'Image': item[0], 'Guess': item[1]})


#classify_folder("/home/andy/images/")
#write()