# скрипт на таминг с дидом у вендора. Время от времени хавает фишстейки, работает только
# если в паке голды больше чем указано значение MinGoldAmount. Берёт из пака дид
# животного, кидает на вендора, (если дидов нет, ищет AnimalType в радиусе 10 тайтлов)
# тамит - стеблит. Ставит игнор таймер на 5 минут если животное агриться. Информирует о
# количесве голды в паке. Завёт гвардов если отравлен или упал уровень ХП или есть кто
# то красный рядом. Ест рыбу на cure, пьёт ГХ. Перед запуском необходимо указать id
# вендора, тип животного и минимальное количество голды для работы скрипта.
# v0.6 made by 80aX for ZHR


from all import *
from time import time as CurrTime


########################################################################################
# CONFIG

VendorID = 0x000E5B5C    # id вендора
AnimalType = 0x00EA      # тип животного
MinGoldAmount = 400      # минимальное колво голды в паке
AngryTime = 300          # таймер для сброса игнора (в сек.)

FixedTimer = 0
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
        return


def CheckDanger():
    SetFindDistance(10)
    for DangerColor in range(4, 7):
        if FindNotoriety(-1, DangerColor) > 0:
            AddToSystemJournal('Danger! Calling guards.')
            UOSay('.guards')
            WaitLag(WaitTime, WaitLagTime)
    return


def CheckPoison():
    if not Poisoned():
        return
    else:
        AddToSystemJournal('Character has been poisoned.')
        UOSay('.guards')
        if FindType(0x0DD6 , Backpack()) > 0:
            UseObject(FindItem())
        WaitLag(WaitTime, WaitLagTime)
        return


def CheckHPLevel():
    if GetHP(Self()) == GetMaxHP(Self()):
        return
    else:
        AddToSystemJournal('Low HP level, probably character has been attacked.')
        UOSay('.guards')
        if GetHP(Self()) < GetMaxHP(Self()) / 2:
            if FindType(0x0F0C, Backpack()) > 0:
                UseObject(FindItem())
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


def CheckIgnoreTimer():
    global FixedTimer
    if FixedTimer == 0:
        return
    else:
        if (CurrTime() - FixedTimer) < AngryTime:
            TimeToReset = int(AngryTime - (CurrTime() - FixedTimer))
            AddToSystemJournal('Ignore reset in {0} sec.'.format(TimeToReset))
            return
        else:
            AddToSystemJournal('Resetting ignore list.')
            FixedTimer = 0
            IgnoreReset()
            return

########################################################################################
# MAIN FUNCTIONS

def Stable(AnimalToStable):
    WaitTargetObject(AnimalToStable)
    UOSay('stable')
    WaitLag(WaitTime, WaitLagTime)
    return True


def Taming(AnimalToTame):
    global FixedTimer
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
            WaitLag(WaitTime, WaitLagTime)
            Ignore(AnimalToTame)
            AddToSystemJournal('Could not tame an animal.')
            FixedTimer = CurrTime()
            AddToSystemJournal('Attention! Set new ignore timer.')
            WaitLag(WaitTime, WaitLagTime)
            break
    return False


def AnimalLore():
    WaitTargetObject(VendorID)
    UseSkill('Animal Lore')
    WaitLag(WaitTime * 18, WaitLagTime)
    return


def CheckAnimal():
    SetFindDistance(10)
    FindType(AnimalType, Ground())
    if FindCount() > 0:
        return True
    else:
        AddToSystemJournal('Could not find an animal on the ground.')
        WaitLag(WaitTime, WaitLagTime)
        return False


def CheckDeed():
    FindType(0x14F0, Backpack())
    if FindCount() > 0:
        DragItem(FindItem(), 1)
        WaitLag(WaitTime, WaitLagTime)
        DropItem(VendorID, 0, 0, 0)
        WaitLag(WaitTime * 4, WaitLagTime)
        return True
    else:
        AddToSystemJournal('Could not find a deed in backpack.')
        WaitLag(WaitTime, WaitLagTime)
        return False


def CheckGold():
    FindType(0x0EED, Backpack())
    AddToSystemJournal('Current gold amount: {0}'.format(FindFullQuantity()))
    if FindFullQuantity() > MinGoldAmount:
        return True
    else:
        AddToSystemJournal('Not enough gold in backpack.')
        WaitLag(WaitTime * 4, WaitLagTime)
        return False

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
            CancelTarget()
            CheckIgnoreTimer()
            if CheckGold() == False:
                AnimalLore()
                continue
            if CheckDeed() == False and CheckAnimal() == False:
                AnimalLore()
                continue
            CurrentAnimal = FindType(AnimalType, Ground())
            UOSay('all release')
            WaitLag(WaitTime, WaitLagTime)
            if Taming(CurrentAnimal) == True:
                Stable(CurrentAnimal)
    return


if __name__ == "__main__":
    main()