from all import Hungry, CheckSave


def tracking():
    CancelMenu()
    WaitMenu('category', '(0)')
    WaitMenu('creature', '(0)')
    UseSkill('Tracking')
    return


def main():
    SetARStatus(True)
    while Connected and (not Dead()):
        Hungry()
        for i in range(100):
            CheckSave()
            tracking()
            Wait(10000)
    return


if __name__ == "__main__":
    main()