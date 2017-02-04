from datetime import datetime, timedelta

def CheckSave():
    Time = datetime.now() - timedelta(0, 30)
    if InJournalBetweenTimes('Сохранение мира.', Time, datetime.now()) >= 0:
        Wait(10000)