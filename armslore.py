from all import Hungry, CheckSave


def ArmsLore():
    CancelTarget()
    CancelWaitTarget()
    WaitTargetObject(FindType(0x0F51,Backpack()))
    UseSkill('Arms Lore')
    Wait(10000)
    return

    
def main():
    SetARStatus(True)
    while Connected and (not Dead()):
        Hungry()
        Wait(1000)
        for i in range(100):
            CheckSave()
            ArmsLore()
    return


if __name__ == "__main__":
    main()