'''
Python script to perform an api upload of a single file into the HIEv application.

Author: Gerard Devine
'''

import os
from datetime import date, datetime, timedelta
import re
import requests
import shutil


# -------------------------------------------------------------------------
# Set metadata variables for upload
api_token        = os.environ['HIEV_API_KEY']
experiment_id     = 1
upload_url        = 'https://ic2-dc21-staging-vm.intersect.org.au/data_files/api_create.json?auth_token='+api_token
# upload_url       = 'https://hiev.uws.edu.au/data_files/api_create.json?auth_token='+api_token
filetype          = 'RAW'
description       = "This is a dummy description for file upload testing"
creator_email     = 'g.devine@westernsydney.edu.au'
contributor_names = ['Tom Smith, t.smith@google.com', 'Jane White, J.White@aol.com', 'Frank Blank, f.black@yahoo.com']
label_names       = '"Rainfall","Environment","TOA5"'
grant_numbers     = '"ZXY7654","PRQ53422"'
related_websites  = '"http://www.bom.org.au","http://www.westernsydney.edu.au"'
start_time        = '2014-01-01 12:11:10'
end_time          = '2014-12-30 14:09:08' 
# -------------------------------------------------------------------------

# Append api token to base URL to generate full HIEv upload API request  

	    
# load the file for uploading via the HIEv API
files = {'file': open('TEST_TOA5_FILE.dat', 'rb')}
      
# Compile available metadata 
payload = {'type':          filetype, 
           'experiment_id': experiment_id, 
           'start_time':    start_time, 
           'end_time':      end_time, 
           'description':   description,
           'label_names':   label_names,
           'creator_email':   creator_email,
           'contributor_names[]':   contributor_names,
           }

# Upload file and associated metadata to HIEv
requests.packages.urllib3.disable_warnings()   # ignore ssl warnings from python 2.7.5
r = requests.post(upload_url, files=files, data=payload, verify=False)

# Print the outcome of the upload
if r.status_code == 200:
    print 'File successfully uploaded to HIEv'
else:
    print 'ERROR - There was a problem uploading the file to HIEv'
