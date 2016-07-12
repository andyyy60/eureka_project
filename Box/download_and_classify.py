import os, csv
from Box import *

list = []
def download_and_classify(folder_id, download_path, max_downloads):

    # log into Box
    cli = setup()
    folder = get_folder(cli, folder_id)
    root_folder = get_folder(cli, str(folder_id))
    # print 'folder owner: ' + root_folder.owned_by['login']
    folder_name = root_folder['name']
    # print 'folder name: ' + folder_name
    folder_contents = (cli.folder(folder_id=folder_id).get_items(limit=100, offset=0))
    path = download_path + "/{}/".format(folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
    if len(folder_contents) > 0:
        # cli.file(file_id='SOME_FILE_ID').get()['name']
        for item in folder_contents:
            id = item.object_id
            if "file" in str(type(item)):  # If this item is a file, base case
                name = cli.file(file_id=str(id)).get()['name']
                if max_downloads > 0 and ".jpg" in name.lower():  # counter has not reached 0 and has jpg extension
                    if not os.path.isfile(path + name):  # if file does not exist
                        with open(str(path + name), 'wb') as open_file:  # Create image
                            open_file.write(cli.file(file_id=str(id)).content())
                        max_downloads -= 1  # decrease counter
                        print "File {} downloaded".format(name)
                    os.system("python classify.py {} foo > temp.txt".format(path+name))
                    temp = open('temp.txt', 'r').readlines()[1]
                    list.append((path+name, temp))
                    os.remove(path+name)
                elif max_downloads <= 0:
                    print "Success."
                    sys.exit(1)

            elif "folder" in str(type(item)):  # If its a folder, call download function recursively
                download_and_classify(id, path, max_downloads)


def write(list):
    with open("results.csv", 'w') as csvfile:
        fieldnames = ['filename', 'guess']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow({'filename': item[0], 'guess': item[4]})


download_and_classify(7843760661,'/home/andy/PycharmProjects/trial',6)
write(list)


