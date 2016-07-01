'''
Python script to perform a API download of the most recent FACE security camera image from HIEv

Author: Gerard Devine
'''

import os
import json
import urllib2
from datetime import date, datetime, timedelta
import time

# --Set up global values
api_token = os.environ['HIEV_API_KEY']
request_url = 'https://hiev.uws.edu.au/data_files/api_search'

# --Provide search filter parameters
filename = 'FACE_R1_P0037_SECURPHOT-TERNsnapshot'
upload_from_date = str(date.today() - timedelta(days=1))
upload_to_date = str(date.today()- timedelta(days=0))

# --Set up the http request
request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
request_data = json.dumps({'auth_token': api_token, 'upload_from_date': upload_from_date, 'upload_to_date': upload_to_date,'filename': filename})

# --Handle the returned response from the HIEv server
# requests.packages.urllib3.disable_warnings()   # ignore ssl warnings from python 2.7.5
request  = urllib2.Request(request_url, request_data, request_headers)
response = urllib2.urlopen(request)
js = json.load(response)
# Grab the latest - in those cases where there are multiple results returned
latest_photo = (sorted(js, key=lambda k: k['updated_at'], reverse=True))[0] 

# --If there are files to be downloaded, then set up a directory to hold them (if not existing)
if len(latest_photo):
    dest_dir = os.path.join(os.path.join(os.path.dirname(__file__), 'data'))
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # --For each element returned pass the url to the download API and download
#     for item in latest_photo:
    download_url = latest_photo['url']+'?'+'auth_token=%s' %api_token
    request = urllib2.Request(download_url)
    f = urllib2.urlopen(request)

    # --Write the file and close it
    with open(os.path.join(dest_dir, latest_photo['filename']), 'w') as local_file:
        local_file.write(f.read())
    local_file.close()

    print 'File successfully downloaded from HIEv'
else:
    print 'ERROR - There was a problem updating the file in HIEv'

