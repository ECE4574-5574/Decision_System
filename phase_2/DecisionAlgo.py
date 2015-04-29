"""Author: Jigar Patel
Date : 4/29/205
Purpose: Generates a decision based on the HISTORY of the ROOM."""

import requests
import json
import os
import httplib


def Decision(lat, longi, alt, userId, timeframe, persistent, server, logger):   
    # Run the URL hosted by server API teams
    url = server         #URL for Server API
    conn = httplib.HTTPConnection(persistent[0], persistent[1])                       #IP Address for Persistent Storage
    # Header for JSON data objects
    headers = {'Content-type': 'application/json'}
    
# Check the room user is in at present, ie if the lat and lon map to a room



# Get the snapshot of devices last time the user was in the room


# Change state of the devices based on the last snapshot of the room

# If there are any manual overrides by the user, update the snapshot entry


# If user moves to another room, take snapshot of the room and store in persistent storage

