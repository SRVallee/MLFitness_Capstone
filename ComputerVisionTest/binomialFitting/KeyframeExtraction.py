#This module is for extracting keyframes from human motion capture. 
#The method was taaken from this paper: http://eprints.bournemouth.ac.uk/35006/1/KeyFrame%2BExtraction%2Bfor%2BHuman%2BMotion%2BCapture.pdf

import math

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
    [0,11,12], [7,12,11],              #nose/neck angle  x, y
    [12,11,13], [23,11,13],            #right shoulder
    [11,12,14], [24,12,14],            #left shoulder
    [11,13,15], [23,13,15],            #right elbow
    [12,14,16], [24,14,16],            #left elbow
    [13,14,19],                        #right wrist 
    [14,16,20],                        #left wrist
    [13,15,21], [17,15,21],            #right thumb
    [14,16,22], [18,16,22],            #left thumb
    [11,23,24],                        #right hip
    [12,24,23],                        #left hip
    [23,25,27], [11,23,25], [24,23,25],#right knee
    [24,26,28], [12,24,26], [23,24,26],#left knee
    [25,27,31], [25,27,29],            #right foot
    [26,28,32], [26,28,30]             #right foot
    ] 

def rSquared():
    return

def getSST():
    return

def getSSR():
    return

#L1, L2, ... Lm 
'''we take time as the independent variable and the
motion information of each dimension of human
joints as dependent variables'''
def plotGraph():
    return

#give the joint and axis
def getAngle(keyPoints, joint, axis): #I will convert this to a list once it's done
    if joint == 0: #nose / neck angle
        if axis == "x":
            #11 and 12 shoulders with nose
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[0],
                keyPoints.pose_landmarks.landmark[11], 
                keyPoints.pose_landmarks.landmark[12])
            
        
        elif axis == "y":
            #a shoulder (11) an ear(7) and the nose(0)
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[7],
                keyPoints.pose_landmarks.landmark[12], 
                keyPoints.pose_landmarks.landmark[11])

        #the way I did it z affects both triangles x and y, but we are measuring for change; It doesn't matter.

    elif joint == 11: #right shoulder
        if axis == "x": 
            #shoulders and right elbow(13)
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[12],
                keyPoints.pose_landmarks.landmark[11], 
                keyPoints.pose_landmarks.landmark[13])

        elif axis == "y":
            #angle between torso shoulder and elbow
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[23],
                keyPoints.pose_landmarks.landmark[11], 
                keyPoints.pose_landmarks.landmark[13])

            #no z axis, this will be the x of the elbow

    elif joint == 12: #left shoulder
        if axis == "x": 
            #shoulders and left elbow(14)
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[11],
                keyPoints.pose_landmarks.landmark[12], 
                keyPoints.pose_landmarks.landmark[14])

        elif axis == "y":
            #angle between torso shoulder and elbow
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[24],
                keyPoints.pose_landmarks.landmark[14], 
                keyPoints.pose_landmarks.landmark[12])

            #no z axis, this will be the x of the elbow

    elif joint == 13: #right elbow
        if axis == "x":
            #11 13 and wrist (15)
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[11],
                keyPoints.pose_landmarks.landmark[13], 
                keyPoints.pose_landmarks.landmark[15])
        
        if axis == "y":
            #23 13 and wrist (15)
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[23],
                keyPoints.pose_landmarks.landmark[13], 
                keyPoints.pose_landmarks.landmark[15])

    
    elif joint == 14: #left elbow
        if axis == "x":
            #12 14 and wrist (16)
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[12],
                keyPoints.pose_landmarks.landmark[14], 
                keyPoints.pose_landmarks.landmark[16])
        
        if axis == "y":
            #24 14 and wrist (16)
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[24],
                keyPoints.pose_landmarks.landmark[14], 
                keyPoints.pose_landmarks.landmark[16])
    #wrists
    elif joint == 15: #right wrist
        if axis == "x":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[13],
                keyPoints.pose_landmarks.landmark[15], 
                keyPoints.pose_landmarks.landmark[19])
        
    elif joint == 16: #left wrist
        if axis == "x":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[14],
                keyPoints.pose_landmarks.landmark[16], 
                keyPoints.pose_landmarks.landmark[20])
    
    #thumbs
    elif joint == 22: #left thumb
        if axis == "x":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[14],
                keyPoints.pose_landmarks.landmark[16], 
                keyPoints.pose_landmarks.landmark[22])
            
        elif axis == "y":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[18],
                keyPoints.pose_landmarks.landmark[16], 
                keyPoints.pose_landmarks.landmark[22])

    elif joint == 21: #right thumb
        if axis == "x":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[13],
                keyPoints.pose_landmarks.landmark[15], 
                keyPoints.pose_landmarks.landmark[21])
        elif axis == "y":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[17],
                keyPoints.pose_landmarks.landmark[15], 
                keyPoints.pose_landmarks.landmark[21])
    #hips 
    elif joint == 23: #right hip
        if axis == "y":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[11],
                keyPoints.pose_landmarks.landmark[23], 
                keyPoints.pose_landmarks.landmark[24])

    elif joint == 24: #left hip
        if axis == "y":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[12],
                keyPoints.pose_landmarks.landmark[24], 
                keyPoints.pose_landmarks.landmark[23])
    #knees
    elif joint == 25: #right knee
        if axis == "x":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[23],
                keyPoints.pose_landmarks.landmark[25], 
                keyPoints.pose_landmarks.landmark[27])
            
        elif axis == "y":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[11],
                keyPoints.pose_landmarks.landmark[23], 
                keyPoints.pose_landmarks.landmark[25])
        
        elif axis == "z":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[24],
                keyPoints.pose_landmarks.landmark[23], 
                keyPoints.pose_landmarks.landmark[25])

    elif joint == 26: #left knee
        if axis == "x":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[24],
                keyPoints.pose_landmarks.landmark[26], 
                keyPoints.pose_landmarks.landmark[28])
        elif axis == "y":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[12],
                keyPoints.pose_landmarks.landmark[24], 
                keyPoints.pose_landmarks.landmark[26])

        elif axis == "z":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[23],
                keyPoints.pose_landmarks.landmark[24], 
                keyPoints.pose_landmarks.landmark[26])

    #feet
    elif joint == 27: #right foot
        if axis == "x":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[25],
                keyPoints.pose_landmarks.landmark[27], 
                keyPoints.pose_landmarks.landmark[31])
            
        elif axis == "y":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[25],
                keyPoints.pose_landmarks.landmark[27], 
                keyPoints.pose_landmarks.landmark[29])

    elif joint == 28: #left foot
        if axis == "x":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[24],
                keyPoints.pose_landmarks.landmark[28], 
                keyPoints.pose_landmarks.landmark[32])
        elif axis == "y":
            return getAnglesFromSides(
                keyPoints.pose_landmarks.landmark[24],
                keyPoints.pose_landmarks.landmark[28], 
                keyPoints.pose_landmarks.landmark[30])


    elif not joint: #Overall rotation relative to the camera
        if axis == "x":
            landmark1 = keyPoints.pose_landmarks.landmark[23]
            landmark2 = keyPoints.pose_landmarks.landmark[24], 
            a = getDistance(landmark1, landmark2)
            b = math.dist([landMark2.x, landMark2.y, landMark2.z], [landMark2.x + 1, landMark2.y, landMark2.z])
            c = math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x + 1, landMark2.y, landMark2.z])
            if c == a+b:
                return 180
            elif c == 0:
                return 0

            return math.degrees(math.acos(((a*a)+(b*b)-(c*c))/(2*a*b)))
                
        elif axis == "y":
            landmark1 = keyPoints.pose_landmarks.landmark[11]
            landmark2 = keyPoints.pose_landmarks.landmark[23], 
            a = getDistance(landmark1, landmark2)
            b = math.dist([landMark2.x, landMark2.y, landMark2.z], [landMark2.x, landMark2.y + 1, landMark2.z])
            c = math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x, landMark2.y + 1, landMark2.z])
            if c == a+b:
                return 180
            elif c == 0:
                return 0

            return math.degrees(math.acos(((a*a)+(b*b)-(c*c))/(2*a*b)))

        elif axis == "z":
            landmark1 = keyPoints.pose_landmarks.landmark[11]
            landmark2 = keyPoints.pose_landmarks.landmark[23], 
            a = getDistance(landmark1, landmark2)
            b = math.dist([landMark2.x, landMark2.y, landMark2.z], [landMark2.x, landMark2.y, landMark2.z + 1])
            c = math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x, landMark2.y, landMark2.z + 1])
            if c == a+b:
                return 180
            elif c == 0:
                return 0

            return math.degrees(math.acos(((a*a)+(b*b)-(c*c))/(2*a*b)))

#get all angles
def getAllAngles(keypoints):
    anglesInFrame = []
    for joint in jointsToMeasure:
        anglesInFrame.append(getAnglesFromSides(
            keyPoints.pose_landmarks.landmark[joint[0]],
            keyPoints.pose_landmarks.landmark[joint[1]], 
            keyPoints.pose_landmarks.landmark[joint[2]]))
    
    
    landmark1 = keyPoints.pose_landmarks.landmark[23]
    landmark2 = keyPoints.pose_landmarks.landmark[24], 
    a = getDistance(landmark1, landmark2)
    b = math.dist([landMark2.x, landMark2.y, landMark2.z], [landMark2.x + 1, landMark2.y, landMark2.z])
    c = math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x + 1, landMark2.y, landMark2.z])
    if c == a+b:
        anglesInFrame.append(180)
    elif c == 0:
        anglesInFrame.append(0)
    else:
        anglesInFrame.append(math.degrees(math.acos(((a*a)+(b*b)-(c*c))/(2*a*b))))
            
    landmark1 = keyPoints.pose_landmarks.landmark[11]
    landmark2 = keyPoints.pose_landmarks.landmark[23], 
    a = getDistance(landmark1, landmark2)
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

