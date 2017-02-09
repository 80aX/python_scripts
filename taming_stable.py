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

VendorID = 0x000E5599    # id вендора
AnimalType = 0x0124      # тип животного
MinGoldAmount = 400      # минимальное колво голды в паке
AngryTime = 330          # таймер для сброса игнора (в сек.)

FixedTimer = 0
WaitTime = 500
LagTime = 5000

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
    SetFindDistance(12)
    if FindNotoriety(-1, 6) > 0:
        AddToSystemJournal('Danger! Calling guards.')
        UOSay('.guards')
        WaitLag(WaitTime, LagTime)
    return


def CheckPoison():
    if not Poisoned():
        return
    else:
        AddToSystemJournal('Character has been poisoned.')
        UOSay('.guards')
        if FindType(0x0DD6 , Backpack()) > 0:
            UseObject(FindItem())
        WaitLag(WaitTime, LagTime)
        return


def CheckHPLevel():
    if GetHP(Self()) == GetMaxHP(Self()):
        return
    else:
        AddToSystemJournal('Low HP level, probably character has been attacked.')
        UOSay('.guards')
        if FindType(0x0F0C , Backpack()) > 0:
            UseObject(FindItem())
        WaitLag(WaitTime, LagTime)
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
    WaitLag(WaitTime, LagTime)
    return True


def Taming(AnimalToTame):
    global FixedTimer
    k = 0
    while k < 10:
        k = k + 1
        CheckStates()
        ClearJournal()
        AddToSystemJournal('Taming try № {0}'.format(k))
        WaitTargetObject(AnimalToTame)
        UseSkill('Animal Taming')
        WaitLag(WaitTime * 20, LagTime)
        if InJournal('successfully') > 0 or InJournal('already') > 0:
            WaitLag(WaitTime, LagTime)
            return True
        elif InJournal('unresponsive') > 0 or InJournal('within your line') > 0:
            WaitLag(WaitTime, LagTime)
            Ignore(AnimalToTame)
            AddToSystemJournal('Could not tame an animal.')
            FixedTimer = CurrTime()
            AddToSystemJournal('Attention! Set new ignore timer.')
            WaitLag(WaitTime, LagTime)
            break
    return False


def AnimalLore():
    WaitTargetObject(VendorID)
    UseSkill('Animal Lore')
    WaitLag(WaitTime * 18, LagTime)
    return


def CheckAnimal():
    SetFindDistance(12)
    FindType(AnimalType, Ground())
    if FindCount() > 0:
        return True
    else:
        AddToSystemJournal('Could not find an animal on the ground.')
        WaitLag(WaitTime, LagTime)
        return False


def CheckDeed():
    FindType(0x14F0, Backpack())
    if FindCount() > 0:
        DragItem(FindItem(), 1)
        WaitLag(WaitTime, LagTime)
        DropItem(VendorID, 0, 0, 0)
        WaitLag(WaitTime * 4, LagTime)
        return True
    else:
        AddToSystemJournal('Could not find a deed in backpack.')
        WaitLag(WaitTime, LagTime)
        return False


def CheckGold():
    FindType(0x0EED, Backpack())
    AddToSystemJournal('Current gold amount: {0}'.format(FindFullQuantity()))
    if FindFullQuantity() > MinGoldAmount:
        return True
    else:
        AddToSystemJournal('Not enough gold in backpack.')
        WaitLag(WaitTime * 4, LagTime)
        return False

########################################################################################
# SCRIPT BODY

def main():
    ScriptInit()
    SetARStatus(True)
    while True:
        Hungry()
        WaitLag(WaitTime, LagTime)
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
            WaitLag(WaitTime, LagTime)
            if Taming(CurrentAnimal) == True:
                Stable(CurrentAnimal)
    return


if __name__ == "__main__":
    main()