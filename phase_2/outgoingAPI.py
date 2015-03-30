#============================================================================
#API for the devices
#Assignment 5 Team 3

#Revision 1 - 03/25/2015 - Jigar Patel (jigar@vt.edu)

#This API runs on the server hosted by Devices (Team 2)
#We will be using GET/POST/PUT/DELETE HTTP methods to modify the data
#============================================================================

import requests
import json
import os

# Run the URL hosted by server API teams
url = 'http://5574serverapi.azurewebsites.net/api/devicemgr/state/'

# Header for JSON data objects
headers = {'Content-type': 'application/json'}

# Append the device id to the URL to modify state for that particular deviceId
device1_url = url + '1'
device2_url = url + '2'
device3_url = url + '3'

# Modify the state for the deviceId based on decision made by the Decision Making algorithm
data1_json= {
                "deviceId": 1,
                "deviceName": "LIGHT:1",
                "deviceType": 5,
                "spaceId": 4,
                "state": 1
            }

data2_json= {
                "deviceId": 2,
                "deviceName": "THERMOSTAT:1",
                "deviceType": 6,
                "spaceId": 5,
                "state": 1
            }

data3_json= {
                "deviceId": 2,
                "deviceName": "SPRINKLER:1",
                "deviceType": 7,
                "spaceId": 4,
                "state": 0
            }


# POST method to send over data to Device API via the server API
response1 = requests.post(device1_url, data=data1_json, headers=headers)
response2 = requests.post(device2_url, data=data2_json, headers=headers)
response3 = requests.post(device3_url, data=data3_json, headers=headers)


# print response received from the server API; <Response [200]> indicates correct response
print response1
print response2
print response3


