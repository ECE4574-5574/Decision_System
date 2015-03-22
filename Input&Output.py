#device state has changed
    #if device is critical,
    #do CriticalLearningAlgorithm
    #else
    #
def deviceChanged(device, state):
    if isCritical(device):
        criticalAlgorithm(device)
    else:
        generalAlgorithm(device)

# Checks if device type is in list of critical devices
def isCritical(device):
    pass

# Does specific behaviors for device types that function
# in sepecific ways (e.g. thermostats) or need oversight (e.g. door locks)
def criticalAlgorithm(device, state):
    pass
# Runs general learning algorithm
def generalAlgorithm(device, state):
    pass

#Current room user is in        
def userLocationChanged(user, location):
    pass

#When an outside stimilus changes (e.g. weather)
def eventOccurred(event, value):
    pass

#get learned behavior from previous room details given by user
def suggestedRoomChanges(room):
    pass

#get learned behavior from previous time blocks 
def suggestedTimeChanges(TimeOfDay):
    pass

