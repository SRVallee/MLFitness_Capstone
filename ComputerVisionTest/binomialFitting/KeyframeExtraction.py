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
    (0,"x"), (0, "y"),
    (11,"x"), (11, "y"),
    (12,"x"), (12, "y"),
    (13,"x"), (13, "y"),
    (14,"x"), (14, "y"),
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
    #TODO
    #wrists
    #thumbs
    #hips
    #torso
    #knees
    #feet
    #overall relative to the axis...  maybe

            
    return

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

