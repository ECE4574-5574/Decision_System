#============================================================================
#API for the devices
#Assignment 6 Team 3
#
#Author - Ekta Bindlish (ekta@vt.edu) 
#Date - 04/06/2015
#
#Purpose: This function will send device state updates to the server API
#============================================================================

import requests
import json
import os

def runOutgoingAPI(message):
    # Run the URL hosted by server API teams
    url = 'http://5574serverapi.azurewebsites.net/api/devicemgr/state/'

    # Header for JSON data objects
    headers = {'Content-type': 'application/json'}
	
    # Append the device id to the URL to modify state for that particular deviceId
    #device1_url = url + '1'
    device1_url = url + str(message["deviceID"])

    # Toggle the device state
    if (str(message["stateDevice"]) == '1'):
        deviceState = 0;
	else: 
        deviceState = 1;
		
    # Modify the state for the deviceId based on decision made by the Decision Making algorithm
"""	
	data1_json= {
                    "deviceId": 1,
                    "deviceName": "LIGHT:1",
                    "deviceType": 5,
                    "spaceId": 4,
                    "state": 1
                }
"""
	data1_json= {
                    "deviceId": message["deviceID"],
                    "deviceName": message["deviceName"],
                    "deviceType": message["deviceType"],
                    "spaceId": message["spaceID"],
                    "state": deviceState
                }

    # POST method to send over data to the server API
    response1 = requests.post(device1_url, data=data1_json, headers=headers)

    # Print response received from the server API
    print response1

if __name__ == '__main__':
    runOutgoingAPI()