device = None
state  = None
user = None
location = None
event = None
value = None

decisionSystem = DecisionSystem()

decisionSystem.deviceChanged(device, state)
decisionSystem.userLocationChanged(user, location)
decisionSystem.eventOccurred(event, value)
