'''
Python script to perform a HIEv search api call (based on given query parameters) and then an API update of the resultant 
files metadata

Author: Gerard Devine
'''

import os
import json
import urllib2
import requests
from datetime import datetime


# -- Set up global values
api_token = os.environ['HIEV_API_KEY']
search_url = 'https://ic2-dc21-staging-vm.intersect.org.au/data_files/api_search'
update_url = 'https://ic2-dc21-staging-vm.intersect.org.au/data_files/api_update?auth_token='+api_token    

# -- As a sanity check, make sure the number of files found matches what was expected (via the HIEv fontend) before proceeding
numfiles_expected = 1

# -- Set up the http search request and handle the returned response
request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
request_data = json.dumps({'auth_token'  : api_token, 
                           #'experiments' : [21], 
			               'filename'    : 'TEST_TOA5_FILE.dat',
 			               #'upload_from_date'   : '2015-11-16'
			              })
requests.packages.urllib3.disable_warnings()   # ignore ssl warnings from python 2.7.5
request  = urllib2.Request(search_url, request_data, request_headers)
response = urllib2.urlopen(request)
js = json.load(response)

# If there are returned results then proceed to update
if len(js):
    assert (len(js) == numfiles_expected), "Number of files found did not match expected"
    # --For each entry returned pass the file id to the update API as well as the updated metadata
    for entry in js:
        # Pick and choose which fields need to be edited
        payload = {
	    'file_id': entry['file_id'],
	    # 'id': 'manual ID',
	    # 'name': "Renamed_Package_2.zip", 
	    'experiment_id': 2,
	    'description': '''"Tipping bucket" rainfall measurements taken above the canopy in a ring every 15 minutes. Descriptions of the variables contained within the file can be found in the associated HIEv metadata file, 'FACE_MD_RAIN.csv', with further information found at: 
	    http://hie-dm.uws.edu.au/data-preparation/eucface/variable-collection-codes/eucface-md-rain/.''',
	    'label_names': "EucFACE, Tipping Bucket, Rainfall, Climate",
	    # 'title': "An second API updated Title for this package",
	    # 'grant_numbers': '"updated2_labelname_1","updated2_labelname_2"',
	    # 'related_websites': '"http://www.bbc.co.uk","http://intersect.org.au/"',
        # 'parent_filenames': ["FACE_MD_RAIN.csv"],
	    # 'access': 'Private',
	    # 'access_to_all_institutional_users':False,
	    # 'access_to_user_groups':True,
	    # 'access_groups':['Gerry_Test'],
	    # 'access_rights_type': "Open",
	    # 'license': "CC-BY-SA",
	    # 'start_time': (datetime.now()- timedelta(days=600)).strftime('%Y-%m-%d %H:%M:%S'), 
	    # 'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'creator_email': 'g.devine@uws.edu.au',
        'contributor_names[]': ['Tom Smith, t.smith@google.com', 'Jane White, J.White@aol.com', 'Jack Black, jack@tree.com', 'Tom Smith, t.smith@google.com']
	}
        # Update current file with the new file metadata
        r = requests.post(update_url, data=payload, verify=False)

        if r.status_code == 200:
            print 'File successfully updated in HIEv'
        else:
            print 'ERROR - There was a problem updating the file in HIEv'
else:
    print 'ERROR - The number of files did not match'
