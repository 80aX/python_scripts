# скрипт на таминг - киллинг, чар стоит на месте(на респе животного) тамит и убивает
# животных заданного типа. Хавает фишстейки, проверяет количество стрел в паке, пишет
# всякую инфу в системный журнал. Качает трекинг если животных нету.
# v0.2 made by 80aX for ZHR

from all import *

########################################################################################
# CONFIG

AnimalType = 0x00E8      # тип животного
BowType = 0x13B2         # тип лука
ArrowsType = 0x0F3F      # тип стрел

WaitTime = 500
WaitLagTime = 5000

########################################################################################
# ADDITIONAL FUNCTIONS

def WaitLag(WaitTime, LagTime):
    Wait(WaitTime)
    CheckLag(LagTime)
    return


def ScriptInit():
    ClearJournal()
    ClearSystemJournal()
    IgnoreReset()
    CancelTarget()
    CancelWaitTarget()
    return


def CheckDead():
    if not Dead():
        return
    else:
        AddToSystemJournal('Character is dead. Disconnecting.')
        FullDisconnect()


def CheckDanger():
    SetFindDistance(10)
    for DangerColor in range(4, 7):
        if FindNotoriety(-1, DangerColor) > 0:
            AddToSystemJournal('Danger! Enemy detected.')
            WaitLag(WaitTime, WaitLagTime)
    return


def CheckPoison():
    if not Poisoned():
        return
    else:
        AddToSystemJournal('Character has been poisoned.')
        if FindType(0x0DD6 , Backpack()) > 0:
            UseObject(FindItem())
        WaitLag(WaitTime, WaitLagTime)
        return


def CheckHPLevel():
    if GetHP(Self()) == GetMaxHP(Self()):
        return
    else:
        AddToSystemJournal('Low HP level, probably character has been attacked.')
        WaitLag(WaitTime, WaitLagTime)
        return


def CheckStates():
    WaitConnection(5000)
    CheckSave()
    CheckDead()
    CheckDanger()
    CheckPoison()
    CheckHPLevel()
    return


########################################################################################
# MAIN FUNCTIONS


def KillAnimal(AnimalToKill):
    SetWarMode(True)
    while GetHP(AnimalToKill) > 0:
        Attack(AnimalToKill)
        WaitLag(WaitTime * 2, WaitLagTime)
    SetWarMode(False)
    return True


def Taming(AnimalToTame):
    TryCount = 0
    while TryCount < 10:
        TryCount += 1
        CheckStates()
        ClearJournal()
        AddToSystemJournal('Taming try № {0}'.format(TryCount))
        WaitTargetObject(AnimalToTame)
        UseSkill('Animal Taming')
        WaitLag(WaitTime * 20, WaitLagTime)
        if InJournal('successfully') > 0 or InJournal('already') > 0:
            WaitLag(WaitTime, WaitLagTime)
            return True
        elif InJournal('unresponsive') > 0 or InJournal('within your line') > 0:
            AddToSystemJournal('Could not tame an animal.')
            WaitLag(WaitTime, WaitLagTime)
            return True
    return False


def Tracking():
    CloseMenu()
    WaitMenu('category', '(0)')
    WaitMenu('creature', '(0)')
    UseSkill('Tracking')
    WaitLag(WaitTime * 20, WaitLagTime)
    return


def CheckAnimal():
    SetFindDistance(12)
    FindType(AnimalType, Ground())
    if FindCount() > 0:
        return True
    else:
        AddToSystemJournal('Could not find an animal on the ground.')
        WaitLag(WaitTime, WaitLagTime)
        return False


def CheckWeapon():
    FindType(ArrowsType, Backpack())
    AddToSystemJournal('Arrows left: {0}'.format(FindFullQuantity()))
    if FindFullQuantity() == 0:
        AddToSystemJournal('Could not find arrows in backpack. Disconnecting')
        FullDisconnect()
    if not ObjAtLayer(RhandLayer()):
        if FindType(BowType, Backpack()) > 0:
            Equip(RhandLayer(), FindItem())
            WaitLag(WaitTime, WaitLagTime)
        else:
            AddToSystemJournal('Could not find a bow in backpack. Disconnecting')
            FullDisconnect()
    return True


########################################################################################
# SCRIPT BODY

def main():
    ScriptInit()
    SetARStatus(True)
    while True:
        Hungry()
        WaitLag(WaitTime, WaitLagTime)
        for i in range(100):
            CheckStates()
            CheckWeapon()
            CancelTarget()
            if CheckAnimal() == False:
                Tracking()
                continue
            CurrentAnimal = FindType(AnimalType, Ground())
            WaitLag(WaitTime, WaitLagTime)
            if Taming(CurrentAnimal) == True:
                KillAnimal(CurrentAnimal)
    return


if __name__ == "__main__":
    main()