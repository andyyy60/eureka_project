'''Authors: Chandra Krintz, Andy Rosales Elias UCSB, ckrintz@cs.ucsb.edu, andy00@umail.ucsb.edu AppScale BSD license'''
import os,sys,json,argparse
from boxsdk.exception import BoxOAuthException
from boxsdk.exception import BoxAPIException
from requests.exceptions import ConnectionError
from boxsdk import OAuth2
from boxsdk import Client
import OpenSSL

DEBUG = False
TOKENS = 'tokens.json'
#############################
def store_tokens(access_token, refresh_token):
    # store the tokens on disk
    data = {
        'access_token' : access_token,
        'refresh_token' : refresh_token,
    }
    with open(TOKENS, 'w') as outfile:
        json.dump(data, outfile)

#############################
def get_tokens() :
    # get the tokens from disk
    data = None
    try:
        data = json.loads(open(TOKENS).read())
    except Exception as e:
        pass
    return data

#############################
def get_folder(client,fid):
    folder = client.folder( folder_id=fid, ).get()
    return folder

#############################
def get_file(client,fid):
    f = client.file( file_id=fid, ).get()
    return f

#############################
def get_files(client,fid,fname,start_with=0,num_results=20):
    ''' given an oauth client, a box folder ID (base), and a filename, search box and return the file object list
        returns list unordered, not guaranteed to have fname in it, sometimes returns nothing
	- not very useful; requires tons of error handling/checking
    '''
    #client.search does not work, returns first file found does not have same fname
    search_results = client.search(
        fname, #name prefixes work (returns multiple)
        limit=num_results,
        offset=start_with,
        ancestor_folders=[client.folder(folder_id=fid)],
        #result_type="file",  #add this if you only want files, without it, this will return files and folders
        #file_extensions=".JPG", doesn't work (nothing returned)
    )
    if DEBUG:
        print 'number of search results {0}'.format(len(search_results))

    return search_results

#############################
def auth():
    # Read app info from text file
    try:
        with open('app.cfg', 'r') as app_cfg:
            client = app_cfg.readline().strip()
            secret = app_cfg.readline().strip()
            redir_uri = app_cfg.readline().strip()
    except:
        print 'Unable to read app.cfg file'
        sys.exit(1)

    if DEBUG:
        print 'clientID {0} sec {1} redir {2}'.format(client,secret,redir_uri)

    data = get_tokens() #checks of TOKENS is available and reads from there if so
    if data is not None:
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        if DEBUG:
            print 'tokens: acc {0} ref {1}'.format(access_token,refresh_token)

        oauth = OAuth2(
            client_id=client,
            client_secret=secret,
            access_token=access_token,
            refresh_token=refresh_token,
            store_tokens=store_tokens, #this stores tokens back in TOKENS
        )
    else:

        #create oauth from client, secret
        oauth = OAuth2(
            client_id=client,
            client_secret=secret,
            store_tokens=store_tokens, #this stores tokens back in TOKENS
        )
        auth_url, csrf_token = oauth.get_authorization_url(redir_uri)
        print 'Cut/Paste this URI into the URL box in \
            \na browser window and press enter:\n\n{0}\n'.format(auth_url)
        print 'You should login and authorize use of your account by this app'
        print 'You will then ultimately be redirected to a URL and a page \
            that says "Connection Refused"'
        auth_code = raw_input('Type in the code that appears after \
            "code="\nin the URL box in your browser window, and press enter: ')
        csrf_returned = raw_input('Type in the csrf in the URI: ')
        assert csrf_returned == csrf_token
        access_token, refresh_token = oauth.authenticate(auth_code)

    return oauth

#############################
def setup():
    oauth = auth()
    client = Client(oauth)

    #get the folder of interest
    return client

#############################
def runit(mydir,folder,client,newFName=None):

    #get the list of filenames already in the folder dictionary
    processed_list = ''
    entries = folder['response_object']['entries']
    #respobj = folder.__dict__['_response_object']
    #items = respobj['item_collection']
    #entries = items['entries']
    for ent in entries:
        n = ent['name']
        processed_list += '{0};'.format(n)

    if newFName is not None: #process the file passed in via newFName arg
        #mydir arg in this case holds the full local path and fname
        #newFName is the shortened fname to use on the remote end
        file_to_upload = mydir
        if DEBUG:
            print 'newfname: {0}, filename: {1}'.format(newFName,file_to_upload)
        done = upload_it(folder,file_to_upload,newFName,processed_list)
        if not done: #try again once on error
            upload_it(folder,file_to_upload,newFName,processed_list)

    else:  #process the dir looping through the files recursively
        #if mydir is not a dir, then the user passed in something
        #wrong, this is checked in main
        print 'uploading to folder: {0}'.format(folder['name'])
        print 'dir: {0}'.format(mydir)
        for root, dirs, files in os.walk(mydir):
            for file in files:
                if file.endswith('.JPG') or file.endswith('.jpg'):
                    fname = file.replace(' ', '_')
                    file_to_upload = '{0}/{1}'.format(root,file)
                    done = upload_it(folder, file_to_upload,fname,processed_list)
                    if not done: #try again once on error
                        upload_it(folder, file_to_upload,fname,processed_list)

#############################
def upload_it(folder, file_to_upload,fname,plist_in,plist_out=None):

    if fname in plist_in:
        if DEBUG:
            print 'skipping {0}'.format(fname)
        return True

    #upload it to box
    print 'upload_it: uploading file via API: {0}'.format(fname)
    try:
        uploaded_file = folder.upload(file_to_upload,file_name=fname,upload_using_accelerator=True)
    except BoxAPIException as e:
        if e.status == 409: #conflict, file exists
            '''
            There is a delay post upload until we can search for files
            (indexing must happen)
            So we must catch when name already in use and replace with:
            #uploaded_file = ftest.update_contents(fname,upload_using_accelerator=True)
            If the upload is idempotent (files aren't changing) we can just continue
            '''
            if plist_out is not None:
                plist_out.write('{0};'.format(fname))  #append to file upon success
            print 'skipping {0}, already uploaded'.format(fname)
            return True #do nothing
        else:
            print e
            print 'Write error3: {0}'.format(fname)
            return False
    except BoxOAuthException as e:
        print e
        print 'Write error2: {0}'.format(fname)
        return False
    except ConnectionError as e:
        print e
        print 'Write error: {0}'.format(fname)
        return False
    except OpenSSL.SSL.SysCallError as e:
        print e
        print 'Write error0: {0}'.format(fname)
        return False
    print 'upload_it: upload complete: {0}'.format(fname)

    if plist_out is not None:
        plist_out.write('{0};'.format(fname))  #append to file upon success
    return True

#############################


def download(folder_id, download_path,max_downloads):
     # log into Box
    cli = setup()
    folder = get_folder(cli, folder_id)
    root_folder = get_folder(cli, str(folder_id))
    #print 'folder owner: ' + root_folder.owned_by['login']
    folder_name = root_folder['name']
    #print 'folder name: ' + folder_name
    gap = len((cli.folder(folder_id=folder_id).get_items(limit=1000, offset=0)))
    increment = 0
    testSum = 0
    while (gap > 0):
        folder_contents = (cli.folder(folder_id=folder_id).get_items(limit=1000, offset=increment))
        testSum += len(folder_contents)
        gap = len(folder_contents)
        increment+=1000
        path = download_path+"/{}/".format(folder_name)
        if not os.path.exists(path):
             os.makedirs(path)
        if len(folder_contents)>0:
            # cli.file(file_id='SOME_FILE_ID').get()['name']
            for item in folder_contents:
                 id = item.object_id
                 if "file" in str(type(item)): #If this item is a file, base case
                     name = cli.file(file_id=str(id)).get()['name']
                     if max_downloads>0 and ".jpg" in name.lower(): #counter has not reached 0 and has jpg extension
                         if not os.path.isfile(path+name): #if file does not exist
                             with open(str(path+name), 'wb') as open_file: #Create image
                                 open_file.write(cli.file(file_id=str(id)).content())
                                 max_downloads-=1 #decrease counter
                                 print "File {} downloaded".format(name)
                     elif max_downloads<=0:
                         print "Success."
                         sys.exit(1)

                 elif "folder" in str(type(item)):#If its a folder, call download function recursively
                     download(id,path,max_downloads)

def search_download(file, path):
    count = 0
    # log into Box
    cli = setup()
    f = open(file, "r")
    for lines in f:
        print lines
        fixed = lines[:-1]
        results = cli.search(lines,1,0)
        my_id = results[0].object_id
        if not os.path.isfile(path+fixed):  # if file does not exist
            with open(str(path+fixed), 'wb') as open_file:  # Create image
                open_file.write(cli.file(file_id=my_id).content())
                count += 1
                print count

search_download("/home/andy/PycharmProjects/data_collector/src/data/deer.txt","/home/andy/images/new/deer/")
# download(7950045909, '/home/andy/PycharmProjects/data_collector/empty_finder/unlabeled', 1000)