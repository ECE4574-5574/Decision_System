"""Author: Prerana Rane
Date : 4/6/2015
Purpose: Generates a decision based on the location of the users."""

import requests
import json
import os
import httplib


def randomDecision(lat, longi, alt, userId, timeframe):   
    # Run the URL hosted by server API teams
    url = 'http://localhost:8082/api/devicemgr/state/'         #URL for Server API
    conn = httplib.HTTPConnection("54.152.190.217", 8080)                       #IP Address for Persistent Storage
    # Header for JSON data objects
    headers = {'Content-type': 'application/json'}

    # Append the device id to the URL to modify state for that particular deviceId
    device1_url = url + '1'
    device2_url = url + '2'
    device3_url = url + '3'
    
    # Modify the state for the deviceId based on decision made by the Decision Making algorithm and the location received

    if(lat>= 0 and longi >= 0):                                                 #Checks latitude,longitude before making a decision
        print "User is in Room#1"
        print "Turn on devices in Room1"
        data1_json= {
                    "houseId": "WayneManor",
                    "roomId": "Atrium",
                    "deviceId": 1,
                    "deviceName": "LIGHT:1",
                    "deviceType": 5,
                    "spaceId": 4,
                    "state": 1
            }
       
        response = requests.post(device1_url, data=data1_json, headers=headers)  #sends response to the Server API
        conn.request('PATCH', 'C/' + userId + '/' + timeframe + '/' + 'WayneManor' + '/11' + '/1', json.dumps(data1_json))  #sends response to the Persistent Storage
        response2 = conn.getresponse()
        print "Server response"
        print response  
        print "Persistent storage response"                                                        #prints response
        print response2.status
        print response2.read()
    elif(lat < 0 and longi < 0):                                                 #Checks latitude,longitude before making a decision
        print "User is in Room#2"
        print "Turn on devices in Room2"
        data2_json= {
                    "houseId": "WayneManor",
                    "roomId": "Atrium",
                    "deviceId": 2,
                    "deviceName": "THERMOSTAT:1",
                    "deviceType": 6,
                    "spaceId": 5,
                    "state": 1
            }
            
        response = requests.post(device1_url, data=data2_json, headers=headers)  #sends response to the Server API
        conn.request('PATCH', 'C/' + userId + '/' + timeframe + '/' + 'WayneManor' + '/12' + '/2', json.dumps(data2_json))  #sends response to the Persistent Storage
        response2 = conn.getresponse()
        print "Server response"
        print response 
        print "Persistent storage response"                                                          #prints response
        print response2.status
        print response2.read()
    else:                                                 #Checks latitude,longitude before making a decision
        print "User is in Room#3"
        print "Turn on devices in Room3"
        data3_json= {
                    "houseId": "WayneManor",
                    "roomId": "Atrium",
                    "deviceId": 3,
                    "deviceName": "SPRINKLER:1",
                    "deviceType": 7,
                    "spaceId": 4,
                    "state": 0
            }
            
        response = requests.post(device1_url, data=data3_json, headers=headers)  #sends response to the Server API
        conn.request('PATCH', 'C/' + userId + '/' + timeframe + '/' + 'WayneManor' + '/13' + '/3', json.dumps(data3_json))  #sends response to the Persistent Storage
        response2 = conn.getresponse()
        print "Server response"
        print response     
        print "Persistent storage response"                                                     #prints response
        print response2.status
        print response2.read()
        
   