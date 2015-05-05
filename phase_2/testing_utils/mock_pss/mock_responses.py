import json

MOCK_DEVICE_BLOB = '{"state": "on", "manufacturer": "Cyberdyne Systems LTD"}'
MOCK_HOUSE_BLOB = '{"nickname": "The Apartment", "address": "221B Baker St", "lat":37.23512, "lon":-80.41352, "alt":20}'
MOCK_HOUSE_BLOB_ALT = '{"nickname": "Blacksburg", "lat":37.23512, "lon":-80.41352, "alt":2050}'

ROOM_1 = {
        'corner1':[37.229874, -80.417854],
        'corner2':[37.229874, -80.417804],
        'corner3':[37.229824, -80.417804],
        'corner4':[37.229824, -80.417854],
        'alt':2080}

ROOM_2 = {
        'corner1':[37.229874, -80.417804],
        'corner2':[37.229874, -80.417754],
        'corner3':[37.229824, -80.417754],
        'corner4':[37.229824, -80.417804],
        'alt':2080}

ROOM_3= {
        'corner1':[37.229874, -80.417754],
        'corner2':[37.229874, -80.417704],
        'corner3':[37.229824, -80.417704],
        'corner4':[37.229824, -80.417754],
        'alt':2080}
        
ROOM_4= {
        'corner1':[37.229874, -80.417704],
        'corner2':[37.229874, -80.417654],
        'corner3':[37.229824, -80.417654],
        'corner4':[37.229824, -80.417704],
        'alt':2080}

def getMockResponse(query, id):
    if query == 'HD' or query == 'RD':
        return json.dumps([{'device-id':'G7Umyvw7cUyxYx9ezuPLDw', 'device-type':'light', 'blob':MOCK_DEVICE_BLOB}, 
                           {'device-id':'nzqnOd3DikipN8spJxE5nQ', 'device-type':'stereo', 'blob':MOCK_DEVICE_BLOB}, 
                           {'device-id':'5CILH42iOU2qF1DiHCLEjg', 'device-type':'thermostat', 'blob':MOCK_DEVICE_BLOB}, 
                           {'device-id':'olnQYPjfJUyijwhY71sxQw', 'device-type':'light', 'blob':MOCK_DEVICE_BLOB}])
    elif query == 'RT' or query == 'RD':
        return json.dumps([{'device-id':'G7Umyvw7cUyxYx9ezuPLDw', 'device-type':'light', 'blob':MOCK_DEVICE_BLOB},
                           {'device-id':'olnQYPjfJUyijwhY71sxQw', 'device-type':'light', 'blob':MOCK_DEVICE_BLOB}])
    elif query == 'BH':
        if id == '101':
            return MOCK_HOUSE_BLOB_ALT
        else:
            return MOCK_HOUSE_BLOB
    elif query == 'BU':
        if id == 'bsaget':
            return json.dumps({'userID': 'bsaget', 'user-full-name': 'Bob Saget', 'houseIDs':[1,101]})
    elif query == 'AL' or query == 'AT' or query == 'CI' or query == 'CT' or query == 'CI':
        return json.dumps([{'time':'2015-03-27T21:07:46Z', 'blob':'light-on'}, 
                           {'time':'2015-03-27T21:07:49Z', 'blob':'light-off'}, 
                           {'time':'2015-03-27T21:07:50Z', 'blob':'light-on'}, 
                           {'time':'2015-03-27T21:07:41Z', 'blob':'light-off'}])
    elif query == 'HR':
        if id == '101':
            return json.dumps({'roomIDs':[1,2,3,4]})
        else:
            return json.dumps({'roomIDs':[]})
    elif query == 'BR':
        print id
        if id[0] == '101':
            if id[1] == '1':
                return json.dumps(ROOM_1)
            if id[1] == '2':
                return json.dumps(ROOM_2)
            if id[1] == '3':
                return json.dumps(ROOM_3)
            if id[1] == '4':
                return json.dumps(ROOM_4)
            
    else:
        return json.dumps({'fake-attribute':'fake-data'})
