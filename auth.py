from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
'''try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
proxy = urllib2.ProxyHandler({'http':'edcguest:edcguest@172.31.100.14:3128', 'https':'edcguest:edcguest@172.31.100.14:3128'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)'''
class auth :
    def __init__(self, SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME) :
        self.SCOPES=SCOPES
        self.CLIENT_SECRET_FILE=CLIENT_SECRET_FILE
        self.APPLICATION_NAME=APPLICATION_NAME
    def getCredentials(self):
        cwd_dir=os.getcwd()
        #home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(cwd_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'google-drive-credentials.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
