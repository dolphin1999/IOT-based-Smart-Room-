from __future__ import print_function
import httplib2
import os,io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import auth
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
'''try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
proxy = urllib2.ProxyHandler({'http':'edcguest:edcguest@172.31.100.14:3128', 'https':'edcguest:edcguest@172.31.100.14:3128'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)'''
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst=auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials=authInst.getCredentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)

def getFiles(size) :
    results = service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def uploadFile(filename,filepath,mimetype) :
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

def downloadFile(file_id,filepath,mimetype) :
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f :
        fh.seek(0)
        f.write(fh.read())
def searchFiles(size,query) :
    results = service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Searched Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))
def delete_file(file_id) :
    service.files().delete(fileId=file_id).execute()
    print('File deleted successfully')
    print('remaining files are :')
    getFiles(500)

getFiles(500)
#uploadFile('Status.txt','Status.txt','text/plain')
#downloadFile('19-Tug1GQKqO0E_3Lyyt-REfDc5IDidkE','downloadedStatus.txt','text/plain')
#searchFiles(500,'name contains "Status"')
#delete_file('1OAg9ZXES2nSpJWplvbG5m0K3IqL0cHDU')
