class Locks:
def __init__(self):
        self.stateList = [] 
	#checks to verify the device ID refers to a specific lock
	#Checks to see if the door is locked or unlocked from Cache
	#return status	
    def LockStatus(self,state,device)
	pass
	
	#When doors are unlocked get learned behavior from previous time blocks based on previous information. And lock door based from user
	#returns the deviceID and state 
    def LockDoor(self, state, device)
	pass
		
	##When doors are locked get learned behavior from previous time blocks based on previous information. Then unlocks door based on user
	#returns deviceID & state 	
    def UnlockDoor(self, state, device)
	pass
