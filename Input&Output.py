#1)Change stateList to a map
#2)When a user enters a room add that room to the map with a corresponding list (map with room as key and list as data)
#3)When user leaves room call a funciton that analyses the list that maps to that room, then remove that key from list



#Graham Cantor-Cooke
class DecisionSystem:
    def __init__(self):
        self.stateList = {}
    # Called when a device state change notification is recieved
    def deviceChanged(self, device, state):
        # Run specialty algorithm
        if isCritical(device):
            criticalAlgorithm(device)
        # Run general learning
        else:
            takeSnapshot(room)
            
    def userLocationChanged(self, user, location):
        #for the new room. Add/updates that rooms state data.
        
        self.stateList[location] = getRoomData(user, location)
		
        try:
            self.previousRoom    #This is in case the previous room has not been defined yet.
        except NameError:
		    self.previousRoom = location
        else:
		    if isempty(previousRoom):
			    emptyRoom(location)
        #it doesn't make sense to delete the previous room from the dictionary.			
	#Checks to see if this room is empty.
	def isempty(self, prevRoom):
	    pass
	#Sets the specified room to its empty state.
	def emptyRoom(self, location):
	    pass
	#Gets the room data.
	def getRoomData(self, user, location):
	    #Return the rooms data as a list.
		pass
    #When an outside stimulus changes (e.g. weather)
    def eventOccurred(self, event, value):
        pass
    # Checks if device type is in list of critical devices
    def isCritical(self, device):
        pass
    
    # Does specific behaviors for device types that function
    # in sepecific ways (e.g. thermostats) or need oversight (e.g. door locks)
    def criticalAlgorithm(self, device, state):
        pass
    # Saves a snapshot of the device states in a room
    def takeSnapshot(room):
        self.stateList[room].append(getFromCache(room))
    
    
    #get learned behavior from previous room details given by user
    def suggestedRoomChanges(self, room):
        pass
    
    #get learned behavior from previous time blocks 
    def suggestedTimeChanges(self, TimeOfDay):
        pass
# Returns the states of the devices in a room with timestamp
getFromCache(room):
    pass
