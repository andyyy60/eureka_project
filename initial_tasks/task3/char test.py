import chandra_ocr, os, csv
directory = os.getcwd()+'/sample_images/'
true = "True"
false = "False"
number_list = [[] for i in range(10)]
with open('info.csv', 'w') as csvfile:
    fieldnames = ['digit', 'filename']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for image in os.listdir(directory):
        temp = str(chandra_ocr.main(2, str('sample_images/' + image)))
        if "0" in temp:
            number_list[0].append(image)
            print "added 0"
        if "1" in temp:
            number_list[1].append(image)
            print "added 1"
        if "2" in temp:
            number_list[2].append(image)
            print "added 2"
        if "3" in temp:
            number_list[3].append(image)
            print "added 3"
        if "4" in temp:
            number_list[4].append(image)
            print "added 4"
        if "5" in temp:
            number_list[5].append(image)
            print "added 5"
        if "6" in temp:
            number_list[6].append(image)
            print "added 6"
        if "7" in temp:
            number_list[7].append(image)
            print "added 7"
        if "8" in temp:
            number_list[8].append(image)
            print "added 8"
        if "9" in temp:
            number_list[9].append(image)
            print "added 9"
    writer.writeheader()
    for n in range(len(number_list)):
        for i in number_list[n]:
            writer.writerow({'digit': str(n),'filename':str(i)})


