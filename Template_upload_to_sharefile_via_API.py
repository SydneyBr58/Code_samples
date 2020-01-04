import json
import http.client
import os
import mimetypes
import time
import urllib.parse
import urllib
import requests
from requests.auth import HTTPBasicAuth

###############################################################################################
'Author: SydneyBr58'

'''
Purpose: This script authenticates the user so that he is able to upload a file from his machine onto a selected sharefile folder
'''

folder_id = '' # Folder id from Sharefile. This one is a test folder 
local_path = r'' # Path to the file you want to upload to Sharefile
hostname = 'your_domain_name.sharefile.com'

client_id = '' #Your client ID for the selected sharefile subdomain, can be given by the domain admin
client_secret = '' #Your client secret for the selected sharefile subdomain, can be given by the domain admin

username = '' #email address you used to register for the selected sharefile subdomain
password = '' #password for the selected sharefile subdomain


def authenticate(hostname, client_id, client_secret, username, password):
    """ Authenticate via username/password. Returns json token object.
    This is pretty much the sample code provided by Citrix here: https://api.sharefile.com/rest/samples/python.aspx
    With all functions updated to Python 3.X. So no need to change this piece of code 

    Providing both password and client_secret makes it not the most secured way to authenticate...
 
    Args:
    string hostname - hostname like "myaccount.sharefile.com"
    string client_id - OAuth2 client_id key
    string client_secret - OAuth2 client_secret key
    string username - my@user.name
    string password - my password """
 
    uri_path = '/oauth/token'
     
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    params = {'grant_type':'password', 'client_id':client_id, 'client_secret':client_secret,
              'username':username, 'password':password}
     
    http4 = http.client.HTTPSConnection(hostname)
    http4.request('POST', uri_path, urllib.parse.urlencode(params), headers=headers)
    response = http4.getresponse()
     
    print(response.status, response.reason)
    token = None
    if response.status == 200:
        token = json.loads(response.read())
        print('Received token info', token)

    return token


def multipart_form_post_upload(url, filepath):
    """ Does a multipart form post upload of a file to a url. This is a modified version of the code sample which can be found on Citrix website (deprecated Python libraries)
    Used to upload the file, nothing to change here, normally 
    This is pretty much the sample code provided by Citrix here: https://api.sharefile.com/rest/samples/python.aspx
    With all functions updated to Python 3.X. So no need to change this piece of code 

    Args:
    string url - the url to upload file to
    string filepath - the complete file path of the file to upload like, "c:\path\to\the.file
     
    Returns:
    the http response """
     
    newline = '\r\n'
    filename = os.path.basename(filepath)
    data = []
    headers = {}
    boundary = '----------%d' % int(time.time())
    headers['content-type'] = 'multipart/form-data; boundary=%s' % boundary
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('File1', filename))
    data.append('Content-Type: %s' % get_content_type(filename))
    data.append('')
    data.append(open(filepath, 'r').read())
    data.append('--%s--' % boundary)
    data.append('')
    data_str = newline.join(data)
    headers['content-length'] = len(data_str)
     
    uri = urllib.parse.urlparse(url)
    http3 = http.client.HTTPSConnection(uri.netloc)
    http3.putrequest('POST', '%s?%s'%(uri.path, uri.query))

    for hdr_name, hdr_value in headers.items():
        http3.putheader(hdr_name, hdr_value)
    http3.endheaders()
    http3.send(str.encode(data_str))
    return http3.getresponse()


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def upload_to_citrix_sharefile(local_path, folder_id, OAuth2_access_token):
    '''
    This function performs the upload of a file, given its path (local_path) and upload it to a Citrix sharefile folder, defined by the hostname and the uri_path
    The upload is done in two steps: first the a GET request is sent to the folder, with an authentication. If this is successful, the server will return an url (upload_config['ChunkUri']) 
    which can be passed to a POST request for the real upload of the file. This is a modified version of the code sample which can be found on Citrix website (deprecated Python libraries)
    
    local path (string): path on your local machine, to the file you want to upload. Use a raw string or \\
    folder_id (string): ID to locate in which folder you want to upload the file. It looks like foxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx and can be found in the url of the folder on Sharefile
    OAuth2_access_token (string): acess token, generated by the function 'authenticate', will be different every time
    '''
    
    header = {'Authorization': 'Bearer '+OAuth2_access_token} 
    uri_path = '/sf/v3/Items('+folder_id+')/Upload' #extention of the folder name, to upload to a different folder, change the foxxxxxxxxxxxxx by the one from the folder
    #it is found in the url of the folder
    hostname = 'theglobalfund.sf-api.com' #Stays the same every time
    http2 = http.client.HTTPSConnection(hostname)
    http2.request('GET', uri_path, headers=header) #
    response2 = http2.getresponse()
    upload_config = json.loads(response2.read())
    if 'ChunkUri' in upload_config:
        upload_response = multipart_form_post_upload(upload_config['ChunkUri'], local_path)
        print('upload_response: ', upload_response.status, upload_response.reason)
    else:
        print('No Upload URL received')
        print(upload_config)


upload_to_citrix_sharefile(local_path, folder_id, authenticate(hostname, client_id, client_secret, username, password)['access_token'])