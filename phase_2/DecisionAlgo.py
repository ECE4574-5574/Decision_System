"""Author: Jigar Patel
Date : 4/29/205
Purpose: Generates a decision based on the location of the users."""

import requests
import json
import os
import httplib


def randomDecision(lat, longi, alt, userId, timeframe, persistent, server, logger):   
    # Run the URL hosted by server API teams
    url = server         #URL for Server API
    conn = httplib.HTTPConnection(persistent[0], persistent[1])                       #IP Address for Persistent Storage
    # Header for JSON data objects
    headers = {'Content-type': 'application/json'}
