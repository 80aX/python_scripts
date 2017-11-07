# Общий модуль, включает набор функций используемых большинством скриптов.
# v0.1 made by 80aX for ZHR


from stealth import *
from datetime import datetime, timedelta


def Hungry():
    if not Connected() or Dead():
        AddToSystemJournal("Cannot check hungry state, character is not connected or dead.")
        return 0

    state = [
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

    foodtype = 0x097B
    pcstoeat = 0

    ctime = datetime.now()
    UOSay('.hungry')
    
    if (WaitJournalLine(ctime, '|'.join(state), 10000)):
        for i in range(2, len(state)):
            if InJournalBetweenTimes(state[i], ctime, datetime.now()) > 0:
                pcstoeat = i - 1;
                break
    else:
        AddToSystemJournal('Cannot check hungry state... Lag?')
        return 0

    if pcstoeat > 0:
        for i in range(pcstoeat):
            if not FindType(foodtype, -1):
                AddToSystemJournal("No food found!")
                return 0
            UseObject(FindItem())
            Wait(100)
    return 1


def CheckSave():
    time = datetime.now() - timedelta(0, 30)
    if InJournalBetweenTimes('Сохранение мира.', time, datetime.now()) >= 0:
        Wait(10000)


def WaitConnection(waittime):
    if Connected():
        return
    while not Connected():
        Wait(1000)
    Wait(waittime)


def FullDisconnect():
    SetARStatus(False)
    Disconnect()


def CheckTargetError(lines, checktime):
    # 5 minutes in DateTime = (1.0 * checktime) / 1440 = 0.00347
    ctime = datetime.now() - timedelta(0, 60 * checktime)
    InJournalBetweenTimes('I am already performing another action|doing something', ctime, datetime.now());
    if LineCount() > lines:
        AddToSystemJournal('Error with target. Disconnected')
        ClearJournal()
        Disconnect()
