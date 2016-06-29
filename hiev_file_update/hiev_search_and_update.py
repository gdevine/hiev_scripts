'''
Python script to perform a HIEv search api call (based on given query parameters) and then an API update of the resultant 
files metadata

Author: Gerard Devine
Date: December 2015


- Note: A valid HIEv API key is required  

'''

import os
import json
import urllib2
import requests
from datetime import datetime


# -- Set up global values
request_url = 'https://hiev.uws.edu.au/data_files/api_search'
# Either set your api key via an environment variable (recommended) or add directly below 
# api_token = os.environ['HIEV_API_KEY']
api_token = '8knbLZNqjAf762KMAhXP'


# -- Set up parameters in which to do the HIEv API search call (see dc21 github wiki for full list of choices available)
filenames = '^FACE_R[1-6]_T1_Rain_[0-9]{8}.dat$'
experiment_ids = [21]


# -- As a sanity check, make sure the number of files found matches what was expected (via the HIEv fontend) before proceeding
numfiles_expected = 106


# --Open log file for writing and append date/time stamp into file for a new entry
logfile = 'log.txt'
log = open(os.path.join(os.path.dirname(__file__), logfile), 'a')
log.write('\n----------------------------------------------- \n')
log.write('------------  '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'  ------------ \n')
log.write('----------------------------------------------- \n')


# -- Set up the http request and handle the returned response
request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
request_data = json.dumps({'auth_token'  : api_token, 
                           'experiments' : experiment_ids, 
			               'filename'    : filenames,
# 			               'upload_from_date'   : '2015-11-16'
			   })
request  = urllib2.Request(request_url, request_data, request_headers)
response = urllib2.urlopen(request)
js = json.load(response)

8
log.write(' Number of search results returned = %s \n' %len(js))
# If there are returned results then proceed to update
if len(js):
    assert (len(js) == numfiles_expected), "Number of files found did not match expected"
    # set the update url
    update_url = 'https://hiev.uws.edu.au/data_files/api_update?auth_token='+api_token	
    # --For each entry returned pass the file id to the update API as well as the updated metadata
    for entry in js:
        payload = {
	    'file_id': entry['file_id'],
	    # 'id': 'manual ID',
	    # 'name': "Renamed_Package_2.zip", 
	    # 'experiment_id': 20,
	    'description': '''"Tipping bucket" rainfall measurements taken above the canopy in a ring every 15 minutes. Descriptions of the variables contained within the file can be found in the associated HIEv metadata file, 'FACE_MD_RAIN.csv', with further information found at: 
	    http://hie-dm.uws.edu.au/data-preparation/eucface/variable-collection-codes/eucface-md-rain/.''',
	    'label_names': ['EucFACE, Tipping Bucket, Rainfall'],
	    # 'title': "An second API updated Title for this package",
	    # 'grant_numbers': '"updated2_labelname_1","updated2_labelname_2"',
	    # 'related_websites': '"http://www.bbc.co.uk","http://intersect.org.au/"',
        'parent_filenames': ["FACE_MD_RAIN.csv"],
	    # 'access': 'Private',
	    # 'access_to_all_institutional_users':False,
	    # 'access_to_user_groups':True,
	    # 'access_groups':['Gerry_Test'],
	    # 'access_rights_type': "Open",
	    # 'license': "CC-BY-SA",
	    # 'start_time': (datetime.now()- timedelta(days=600)).strftime('%Y-%m-%d %H:%M:%S'), 
	    # 'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	}
        # Update current file with the new file metadata
        r = requests.post(update_url, data=payload)
 
    log.write('-- Complete \n')
else:
    log.write('No files matched the search params \n')
    log.write('\n')
    log.write('\n')

# --Close log file
log.close()
