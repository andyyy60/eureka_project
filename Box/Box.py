import urllib

import requests
from boxsdk import Client, OAuth2
from boxsdk.network.default_network import DefaultNetwork
from pprint import pformat
from PIL import Image


CLIENT_ID     = ''
CLIENT_SECRET = ''
ACCESS_TOKEN  = ''
AUTH_CODE = ''


class LoggingNetwork(DefaultNetwork):
    def request(self, method, url, access_token, **kwargs):
        """ Base class override. Pretty-prints outgoing requests and incoming responses. """
        print '\x1b[36m{} {} {}\x1b[0m'.format(method, url, pformat(kwargs))
        response = super(LoggingNetwork, self).request(
            method, url, access_token, **kwargs
        )
        if response.ok:
            print '\x1b[32m{}\x1b[0m'.format(response.content)
        else:
            print '\x1b[31m{}\n{}\n{}\x1b[0m'.format(
                response.status_code,
                response.headers,
                pformat(response.content),
            )
        return response

oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN)
client = Client(oauth2, LoggingNetwork())


with open('open.jpg', 'wb') as open_file:
    open_file.write(client.file(file_id='66046362001').content())
