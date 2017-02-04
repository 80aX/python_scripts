# hungry.py Модуль проверки голода.
# Вызывается hungry(). Кушает жареную рыбу до состояния 'You are stuffed'.

from datetime import datetime as dt
# from stealth import *

def Hungry():
	if not Connected() or Dead():
		AddToSystemJournal("Cannot check hungry state, character is not connected or dead.")
		return 0

	State = [
		'You are absolutely stuffed!',
		'You are stuffed',
		'hungry at all',
		'You are a little hungry',
		'You are somewhat hungry',
		'You are REALLY hungry',
		'Your stomach hurts',
		'Your stomach hurts and you feel dizzy',
		'You are starving',
		'You are almost dying of hunger',
		'You are DYING of hunger...'
	]

	FoodType = 0x097B
	PcsToEat = 0

	ctime = dt.now()
	UOSay('.hungry')
	Wait(100)
	
	for i in range(len(State)):
		if InJournalBetweenTimes(State[i], ctime, dt.now()) > 0:
			PcsToEat = i - 1;
			break
	else:
		AddToSystemJournal('Cannot check hungry state... Lag?')
		return 0
      
	if PcsToEat > 0:
		for i in range(PcsToEat):
			if FindType(FoodType, -1) <= 0:
				AddToSystemJournal("No food found!")
				return 0
			UseObject(FindItem())
			Wait(100)
	return 1
