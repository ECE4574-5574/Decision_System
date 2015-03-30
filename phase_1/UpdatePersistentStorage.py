#Contributor : Prerana Rane
#Learned behaviours will be stored in the Persistent Storage in the form of Device States
#This will be called after the user's preferences are decided.

import sqlite3

conn = sqlite3.connect('device.sqlite3')
cur = conn.cursor()   #Opens the database connection

#If a New Device is added, add a new row in the table 'Devices' and store the state of the device
#Depends on the tables created and the structure of the table.
cur.execute('INSERT INTO Devices (DeviceID,State, timestamp) VALUES ( ?, ?, ?)', 
    ( 'Light', 'ON', sysdate ) )

#Will be a generic function for all the state changes.    
#If learned behaviour is decided    
#Update the database and store the state    
cur.execute('UPDATE Devices (DeviceID,State, timestamp)  VALUES ( ?, ? )', 
    ( 'Light', 'OFF', sysdate ) )
conn.commit()

#Displays the devices stored
print 'Devices:'
cur.execute('SELECT DeviceID,State, timestamp FROM Devices')
for row in cur :
   print row

#Commits changes
conn.commit()

#Closes the connection
cur.close()
