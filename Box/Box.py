'''Author: Chandra Krintz, UCSB, ckrintz@cs.ucsb.edu, AppScale BSD license'''
import os, sys, json, argparse
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
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
    with open(TOKENS, 'w') as outfile:
        json.dump(data, outfile)


#############################
def get_tokens():
    # get the tokens from disk
    data = None
    try:
        data = json.loads(open(TOKENS).read())
    except Exception as e:
        pass
    return data


#############################
def get_folder(client, fid):
    folder = client.folder(folder_id=fid, ).get()
    return folder


#############################
def get_file(client, fid):
    f = client.file(file_id=fid, ).get()
    return f


#############################
def get_files(client, fid, fname, start_with=0, num_results=20):
    ''' given an oauth client, a box folder ID (base), and a filename, search box and return the file object list
        returns list unordered, not guaranteed to have fname in it, sometimes returns nothing
	- not very useful; requires tons of error handling/checking
    '''
    # client.search does not work, returns first file found does not have same fname
    search_results = client.search(
        fname,  # name prefixes work (returns multiple)
        limit=num_results,
        offset=start_with,
        ancestor_folders=[client.folder(folder_id=fid)],
        # result_type="file",  #add this if you only want files, without it, this will return files and folders
        # file_extensions=".JPG", doesn't work (nothing returned)
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
        print 'clientID {0} sec {1} redir {2}'.format(client, secret, redir_uri)

    data = get_tokens()  # checks of TOKENS is available and reads from there if so
    if data is not None:
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        if DEBUG:
            print 'tokens: acc {0} ref {1}'.format(access_token, refresh_token)

        oauth = OAuth2(
            client_id=client,
            client_secret=secret,
            access_token=access_token,
            refresh_token=refresh_token,
            store_tokens=store_tokens,  # this stores tokens back in TOKENS
        )
    else:

        # create oauth from client, secret
        oauth = OAuth2(
            client_id=client,
            client_secret=secret,
            store_tokens=store_tokens,  # this stores tokens back in TOKENS
        )
        auth_url, csrf_token = oauth.get_authorization_url(redir_uri)
        print 'Cut/Paste this URI into the URL box in \
            \na browser window and press enter:\n\n{0}\n'.format(auth_url)
        print 'You should login and authorize use of your account by this app'
        print 'You will then ultimately be redirected to a URL and a page \
            that says "Connection Refused"'
        auth_code = raw_input('Type in the code that appears after"code="\nin the URL box in your browser window, and press enter: ')
        csrf_returned = raw_input('Type in the csrf in the URI: ')
        print csrf_token
        assert csrf_returned == csrf_token
        access_token, refresh_token = oauth.authenticate(auth_code)

    return oauth


#############################
def setup():
    oauth = auth()
    client = Client(oauth)

    # get the folder of interest
    return client


def download(folder_id, download_path,max_downloads=0):
     # log into Box
     #TODO: If a file exists, skip
     #TODO: Implement max downloads
    cli = setup()
    folder = get_folder(cli, folder_id)
    root_folder = get_folder(cli, str(folder_id))
    print 'folder owner: ' + root_folder.owned_by['login']
    folder_name = root_folder['name']
    print 'folder name: ' + folder_name
    folder_contents = (cli.folder(folder_id=folder_id).get_items(limit=100, offset=0))
    path = download_path+"/{}/".format(folder_name)
    if not os.path.exists(path):
         os.makedirs(path)
    if len(folder_contents)>0:
        # cli.file(file_id='SOME_FILE_ID').get()['name']
        for item in folder_contents:
             id = item.object_id
             if "file" in str(type(item)): #If this item is a file, base case
                 name = cli.file(file_id=str(id)).get()['name']
                 with open(str(path+name), 'wb') as open_file: #Create image
                     open_file.write(cli.file(file_id=str(id)).content())
             elif "folder" in str(type(item)):#If its a folder, call download function recursively
                 download(id,path)


