def WaitConnection(WaitTime):
    if Connected():
        return
    while not Connected():
        Wait(1000)
    Wait(WaitTime)
	return