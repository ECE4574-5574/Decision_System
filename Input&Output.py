class DecisionSystem:
    def __init__(self):
        self.stateList = []
    # Called when a device state change notification is recieved
    def deviceChanged(self, device, state):
        if isCritical(device):
            criticalAlgorithm(device)
        else:
            generalAlgorithm(device)
    
    # Checks if device type is in list of critical devices
    def isCritical(self, device):
        pass
    
    # Does specific behaviors for device types that function
    # in sepecific ways (e.g. thermostats) or need oversight (e.g. door locks)
    def criticalAlgorithm(self, device, state):
        pass
    # Runs general learning algorithm
    def generalAlgorithm(self, device, state):
        pass
    
    #Current room user is in        
    def userLocationChanged(self, user, location):
        pass
    
    #When an outside stimilus changes (e.g. weather)
    def eventOccurred(self, event, value):
        pass
    
    #get learned behavior from previous room details given by user
    def suggestedRoomChanges(self, room):
        pass
    
    #get learned behavior from previous time blocks 
    def suggestedTimeChanges(self, TimeOfDay):
        pass

