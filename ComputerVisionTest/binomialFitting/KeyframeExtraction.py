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
curve and m is 58.
'''


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
def getAngle(keyPoints, joint, axis):
    if joint == 0: #nose / neck angle
        if axis == "x":
            #11 and 12 shoulders with nose
            #only one is needed, I chose left shoulder (11)
            h = getDistance(keyPoints.pose_landmarks.landmark[0], keyPoints.pose_landmarks.landmark[11])
            a = getDistance(keyPoints.pose_landmarks.landmark[11], keyPoints.pose_landmarks.landmark[12])
            return math.degrees(math.cos((a/2)/h))

            
    return

def getDistance(landMark1, landMark2):

    return math.dist([landMark1.x, landMark1.y, landMark1.z], [landMark2.x, landMark2.y, landMark2.z])

