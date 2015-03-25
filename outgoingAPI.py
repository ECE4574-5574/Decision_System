============================================================================
API for the devices
Assignment 5 Team 3

Revision 1 - 03/25/2015 - Jigar Patel (jigar@vt.edu)
============================================================================


import requests
import json
import restful_webapi
import os

# This example shows how to use the Requests library with RESTful API
# This web service stores arbitrary JSON data under integer keys
# We can use GET/POST/PUT/DELETE HTTP methods to modify the data

# Run a local server that we can use
restful_webapi.run_server()

# post data from the decision algorithm to the Device API
service = 'http://localhost:8080'

created = None
data = json.dumps(DeviceID, DeviceStatus)
params = urllib.urlencode({
  'Device ID': '',
  'Status': ''
})

#if new state
r = requests.post(service, data=data)
#else
r = requests.patch(service, data=data)

# Stop the server and quit
os._exit(0)

