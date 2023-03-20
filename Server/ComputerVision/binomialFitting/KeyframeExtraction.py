#This module is for extracting keyframes from human motion capture. 
#The method was taaken from this paper: http://eprints.bournemouth.ac.uk/35006/1/KeyFrame%2BExtraction%2Bfor%2BHuman%2BMotion%2BCapture.pdf


import math
import statistics
import binomialFitting.PoseUtilities as PoseUtilities

'''
the curve Li is used
to represent the change of rotation of a joint in one direction or the trajectory
of the root joint in one direction.

For each motion
sequence, we can obtain 55 rotation information
curves and 3 motion trajectory curves. Then the
motion sequence is expressed as a set of curves
M = L1, ...Li, ...Lm, where i represents the ith
curve and m is 58. In our case is less
'''

jointsToMeasure = [ #adding them as I make them available
    [0,11,12], [7,12,11],              #nose/neck angle  1,2
    [12,11,13], [23,11,13],            #right shoulder   3,4
    [11,12,14], [24,12,14],            #left shoulder    5,6
    [11,13,15], [23,13,11],            #right elbow      7,8
    [12,14,16], [24,14,12],            #left elbow       9,10
    [13,14,19],                        #right wrist      11
    [14,16,20],                        #left wrist       12
    [13,15,21], [17,15,21],            #right thumb      13,14
    [14,16,22], [18,16,22],            #left thumb       15,16
    [11,23,24],                        #right hip        17
    [12,24,23],                        #left hip         18
    [23,25,27], [11,23,25], [24,23,25],#right knee       19 - 21
    [24,26,28], [12,24,26], [23,24,26],#left knee        22 - 24
    [25,27,31], [25,27,29],            #right foot       25,26
    [26,28,32], [26,28,30]             #right foot       27,28
    #x                                                   29
    #y                                                   30
    #z                                                   31
    ] 

def getSSE(data, f, startX):
    sse = 0

    for i in range(len(data)):
        e = data[i] - (f[0]*(i+startX+1) + f[1])
        sse += e*e
    return sse

def getSSR(data):
    mean = statistics.mean(data)
    ssr = 0
    for i in data:
        ssr += (i - mean)*(i - mean)
    return ssr

def getF(data, startX):
    n = len(data)
    tempTopX = 0
    tempTopXY = 0
    tempTopXX = 0

    for i in range(n):
        x = startX+1 + i
        tempTopX += x
        tempTopXY += (data[i]*x)
        tempTopXX += x*x

    xMean = tempTopX/n
    yMean = statistics.mean(data)
    xyMean = tempTopXY/n
    xxMean = tempTopXX/n

    slope = (xyMean - xMean*yMean)/(xxMean - xMean*xMean)

    b = yMean - slope*xMean

    return (slope, b)


#get all angles
def getAllAngles(keyPoints):
    anglesInFrame = []

    for joint in jointsToMeasure:
        anglesInFrame.append(getAnglesFromSides(
            keyPoints.pose_world_landmarks.landmark[joint[0]],
            keyPoints.pose_world_landmarks.landmark[joint[1]], 
            keyPoints.pose_world_landmarks.landmark[joint[2]]))
    
    
    landMark1 = keyPoints.pose_world_landmarks.landmark[23]
    landMark2 = keyPoints.pose_world_landmarks.landmark[24]
    a = getDistance(landMark1, landMark2)
    b = math.dist([landMark2.x, landMark2.y, landMark2.z], [landMark2.x + 1, landMark2.y, landMark2.z])
    c = math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x + 1, landMark2.y, landMark2.z])
    if c == a+b:
        anglesInFrame.append(180)
    elif c == 0:
        anglesInFrame.append(0)
    else:
        anglesInFrame.append(math.degrees(math.acos(((a*a)+(b*b)-(c*c))/(2*a*b))))
            
    landMark1 = keyPoints.pose_world_landmarks.landmark[11]
    landMark2 = keyPoints.pose_world_landmarks.landmark[23]
    a = getDistance(landMark1, landMark2)
    b = math.dist([landMark2.x, landMark2.y, landMark2.z], [landMark2.x, landMark2.y + 1, landMark2.z])
    c = math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x, landMark2.y + 1, landMark2.z])
    if c == a+b:
        anglesInFrame.append(180)
    elif c == 0:
        anglesInFrame.append(0)
    else:
        anglesInFrame.append(math.degrees(math.acos(((a*a)+(b*b)-(c*c))/(2*a*b))))

    b = math.dist([landMark2.x, landMark2.y, landMark2.z], [landMark2.x, landMark2.y, landMark2.z + 1])
    c = math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x, landMark2.y, landMark2.z + 1])
    if c == a+b:
        anglesInFrame.append(180)
    elif c == 0:
        anglesInFrame.append(0)
    else:
        anglesInFrame.append(math.degrees(math.acos(((a*a)+(b*b)-(c*c))/(2*a*b))))

    return anglesInFrame

def getDistance(landMark1, landMark2):

    return math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x, landMark2.y, landMark2.z])

def getAnglesFromSides(joint1,joint2,joint3): #takes angle at joint2
    a = getDistance(joint1, joint2)
    b = getDistance(joint2, joint3)
    c = getDistance(joint1, joint3)
    if c == a+b:
        return 180
    elif c == 0:
        return 0

    return math.degrees(math.acos(((a*a)+(b*b)-(c*c))/(2*a*b)))

def extractFrames(frames, rSquared, getAngles = False): #Returns simpleModel if getAngles is set to True
    allAngles = []
    keyList = []
    keyAngles = []
    for frame in frames: #fills list with lists of angles
        if frame.pose_world_landmarks:
            allAngles.append(PoseUtilities.compute_body_angles(frame.pose_world_landmarks))
            frames.remove(frame)
        # allAngles.append(getAllAngles(frame))
    n = len(frames)
    keyList.append((frames[0],0))

    simpleModel = simplifiedCurveModel(allAngles)
    f = []
    for i in range(len(simpleModel)):
        f.append((0,simpleModel[i][0])) #start with slope 0 on f(x) = 0x+b
    start = 0
    tempEnd = 1
    end = 0
    count = 0
    while start+1 != n:
        while tempEnd < n:
            count += 1
            smallestR = getMeanRSquared(simpleModel, f, start, tempEnd)
            #print(f"Smallest R squared: {smallestR}")
            if smallestR >= rSquared:
                # print("continuing...")
                #include tempEnd
                end = tempEnd
                tempEnd += 1
                if tempEnd != n:
                    for i in range(len(simpleModel)):
                        curve = simpleModel[i]
                        f[i] = getF(curve[start:tempEnd+1], start)
                
                
            else:
                #save keyframe, change start, and get new binomials
                #print("saving...")
                keyList.append((frames[end], end))
                keyAngles.append(allAngles[end])
                start = tempEnd
                tempEnd += 1
                if start+1 != n:
                    for i in range(len(simpleModel)):
                        curve = simpleModel[i]
                        f[i] = getF(curve[start:tempEnd+1], start)
                    
                
                break
        else:
            break
    print(f"looped: {count} times")
    keyList.append((frames[-1],len(frames)-1))
    
    if keyList[0] == keyList[1]:
        keyList.pop(0)
    if keyList[-1] == keyList[-2]:
        keyList.pop(-1)
    if getAngles:
        return keyList, allAngles, keyAngles
        # return keyList, keyAngles
    return keyList
            

def simplifiedCurveModel(angles): #rearrenges the list of angles to be joint per list rather than frame per list
    #print(f"angles: {angles}")
    m = [[] for i in range(len(angles[0]))]

    for angleSet in angles:
        for i in range(len(angleSet)):
            m[i].append((angleSet[i]))
    return m

#gets smallest RSquared out of the angles
def getSmallestRSquared(simpleModel, f, start, end):
    smallest = 1
    for i in range(len(simpleModel)):
        curve = simpleModel[i]
        sse = getSSE(curve[start:end+1], f[i], start)
        ssr = getSSR(curve[start:end+1])
        rSq = 1 - (sse/ssr)
        # print("\nsse", sse, end=" ")
        # print("\nssr", ssr, end=" ")
        
        if rSq < smallest:
            smallest = rSq
            #print(f"smallest R at frame {i+1}")
        
    return smallest

def getMeanRSquared(simpleModel, f, start, end):
    top = 0
    # print(f"{end}-{start}")
    for i in range(len(simpleModel)):
        curve = simpleModel[i]
        sse = getSSE(curve[start:end+1], f[i], start)
        ssr = getSSR(curve[start:end+1])
        top += (1 - (sse/ssr))
    #     print("\nsse", sse, end=" ")
    #     print("\nssr", ssr, end=" ")
    # print("\ntop", top, end=" ")
    # print(top/(end-start+2))
    return top/(end-start+2)
    