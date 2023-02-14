def hello():
    return "hello darkness"

def HighVis(LmList):
    joint1 = 0
    joint2 = 0
    for i in range(len(LmList)):
        visibilty = float(LmList[i][4])
        print(visibilty)
    return True

def frontorient(LmList):
    for i in range(len(LmList)):
        visibilty = float(LmList[i][4])
        if LmList[i][0] == 11:
            rightShoulder = LmList[i][4]
        elif LmList[i][0] == 23:
            righthip = LmList[i][4]
        elif LmList[i][0] == 12:
            leftShoulder = LmList[i][4]
        elif LmList[i][0] == 24:
            lefthip = LmList[i][4]
    