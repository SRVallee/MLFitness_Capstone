'''

'''
import cv2
import mediapipe as mp
import numpy as np
import math
import json
import statistics
import os
import binomialFitting.KeyframeExtraction as KeyframeExtraction
import mp_drawing_modified
from Workout import Workout
from WorkoutPose import WorkoutPose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

MENU = "Select the joints that cycle separated by commas \n\
    Ex. for push ups: 4,5\n\n\
1   neck\n\
2   right shoulder\n\
3   left shoulder\n\
4   right elbow\n\
5   left elbow\n\
6   right wrist\n\
7   left wrist\n\
8   right hip\n\
9   left hip\n\
10  right knee\n\
11  left knee\n\
12  right foot\n\
13  right foot"

choiceList = {
    "1":    [0,1],
    "2":    [2,3],
    "3":    [4,5],
    "4":    [6,7],
    "5":    [8,9],
    "6":    [10],
    "7":    [11],
    "8":    [16],
    "9":    [17],
    "10":   [18,19,20],
    "11":   [21,22,23],
    "12":   [24,25],
    "13":   [26,27]
}

def getJoint(angle):
    a = int(angle)
    if a in range(10) or a == 12 or a == 13:
        return a//2 +1
    elif a == 10 or a == 11:
        return a - 4
    elif a == 16 or a == 17:
        return a - 8
    elif a == 18 or a == 19 or a == 20:
        return 10
    elif a == 21 or a == 22 or a == 23:
        return 11

def convertJoints(Joints):
    angles = []
    for joint in Joints:
        angles += choiceList[joint]
    angles.sort()
    return angles

from statistics import mean
from statistics import stdev

#parameters
def getKeyFramesFromVideo(video, show = False):
    cap = cv2.VideoCapture(video)
    allFrames = []
    with mp_pose.Pose(
        min_detection_confidence=0.1,
        min_tracking_confidence=0.1) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            allFrames.append(results)
            if show:
                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('MediaPipe Pose', cv2.flip(image, 2))
            if cv2.waitKey(5) & 0xFF == 27:
                break

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    print(f"frames: {len(allFrames)}")
    print(f"framerate: {fps}")

    rSquared = 0.7

    print(f"RSquared: {rSquared}")
    extracted, allangles = KeyframeExtraction.extractFrames(allFrames, rSquared, True)
    print(f"{len(extracted)} frames extracted")
    return extracted, allangles


def getReps(keyFrames, anglesPerFrame, workout = None):
    allAngles = KeyframeExtraction.simplifiedCurveModel(anglesPerFrame)
    if not workout:
        modelName, importantJoints = setupNewWorkout()
        importantAngles = convertJoints(importantJoints)
    else:
        modelName = workout
        model = Workout().loadModel(f"ComputerVisionTest/models/{workout}.json")
        importantAngles = model.getImportantAngles()
    nFrames = len(keyFrames)
    reptypes = [[] for i in range(nFrames)] 
    cycles = [[] for i in range(len(importantAngles))] #[start, turning point, end, angle]
    cycleType = [] #Stores boolean for open type: if angle is closed -> open -> close

    for curve in range(len(importantAngles)): #Only include important Joint angles
        angle1, angle2, increase = None, None, None
        
        #get cycles
        for frame in range(nFrames):

            angle1 = angle2
            angle2 = allAngles[importantAngles[curve]][keyFrames[frame][1]] #all angles includes all Frames, not just keyframes

            if(angle1 != 0 and not angle1): #if first angle
                angle1 = angle2

            else: #get direction change and angle difference
                #if last frame was a decrese and now it's increasing
                if (angle1 < angle2) and increase == False: #can be None
                    increase = True
                    reptypes[frame].append([angle2, curve, increase, angle2 - angle1])

                    if not cycleType[curve]:
                        cycles[curve][-1][2] = frame
                        if cycles[curve][-1][3] < (angle2 - angle1):
                            cycles[curve][-1][3] = angle2 - angle1
                        cycles[curve].append([frame, None, None, angle2 - angle1])
                    else:
                        cycles[curve][-1][1] = frame + 1
                        if cycles[curve][-1][3] < (angle2 - angle1):
                            cycles[curve][-1][3] = angle2 - angle1

                    angle1 = angle2

                #if last frame was an increase and now it's a decrease
                elif (angle1 > angle2) and increase:
                    increase = False
                    reptypes[frame].append([angle2, curve, increase, angle1 - angle2])
                    
                    if cycleType[curve]:
                        cycles[curve][-1][2] = frame
                        if cycles[curve][-1][3] < (angle1 - angle2):
                            cycles[curve][-1][3] = angle1 - angle2
                        cycles[curve].append([frame, None, None, angle1 - angle2])
                    else:
                        cycles[curve][-1][1] = frame + 1
                        if cycles[curve][-1][3] < (angle1 - angle2):
                            cycles[curve][-1][3] = angle1 - angle2

                    angle1 = angle2

                #if comparing with first frame
                elif (increase == None):
                    if angle1 < angle2:
                        increase = True
                        reptypes[frame].append([angle2, curve, increase, angle2 - angle1])
                        reptypes[0].append([angle1, curve, False, 0])
                        cycles[curve].append([0, frame, None, angle2 - angle1]) #Set Values for first time setup.
                        cycleType.append(True)

                        angle1 = angle2

                    
                    else:
                        increase = False
                        reptypes[frame].append([angle2, curve, increase, angle1 - angle2])
                        reptypes[0].append([angle1, curve, True, 0])
                        cycles[curve].append([0, frame, None, angle1 - angle2]) #Set Values for first time setup.
                        cycleType.append(False)
                        angle1 = angle2
                    
    #check important joint changes
    i = 1

    #get reps without model
    if not workout:
        parallel = getTrend(cycles)
    else:
        parallel = getCloser(cycles, keyFrames, anglesPerFrame, model)
    print(f"cycles: {parallel}")

    #for x in cycles:
        
    # for change in reptypes: #debug only
    #     increase = 0
    #     decrease = 0
    #     max = 0
    #     maxFrom = 0
    #     for angle in change:
    #         #print(f"angle change on {angle}: {angle[3]}")
    #         if angle[2]:
    #             increase += 1
    #         else:
    #             decrease += 1
    #         if max < angle[3]:
    #             max = angle[3]
    #             maxFrom = angle[1]
    #     print(f"frame {i} with {len(change)} changes: {increase} increase and {decrease} decrease with a max angle change of {max} from {maxFrom}")

    #     i+=1

    return parallel, modelName, importantAngles

def getTrend(cycles):
    #cycle [start, turning point, end, angle]

    reps = []

    maxLen = 0
    for joint in cycles:
        for cycleJoint in joint:
            if cycleJoint[3] < 5: #remove cycles under 5 degrees
                joint.remove(cycleJoint)
            
                
        if len(joint) > maxLen:
            maxLen = len(joint)
    

    potentialReps = [[] for i in range(maxLen)]


    for joint in  cycles:
        n = 0
        for cycleJoint in joint:
            potentialReps[n].append(cycleJoint)
            n = n + 1
            print(n)

    #print(f"Potential: {potentialReps}")
    
    for cycleGroup in potentialReps: #Take the most common values
        starts = {}
        middle = {}
        end = {} 
        for cycle in cycleGroup:
            print(f"cycle: {cycle}")
            if str(cycle[0]) in starts.keys():
                starts[str(cycle[0])] = starts[str(cycle[0])] + 1
            else:
                starts[str(cycle[0])] = 1

            if str(cycle[1]) in middle.keys():
                middle[str(cycle[1])] = middle[str(cycle[1])] + 1
            else:
                middle[str(cycle[1])] = 1

            if str(cycle[2]) in end.keys():
                end[str(cycle[2])] = end[str(cycle[2])] + 1
            else:
                end[str(cycle[2])] = 1
            
        finalStart = None
        finalMiddle = None
        finalEnd = None
        for start in starts.keys():
            if not finalStart or starts[str(finalStart)] < starts[start]:
                finalStart = int(start)

        for mid in middle.keys():
            if not finalMiddle or middle[str(finalMiddle)] < middle[mid]:
                if mid != "None":
                    finalMiddle = int(mid)
                else:
                    finalMiddle = None

        for ending in end.keys():
            if not finalEnd or end[str(finalEnd)] < end[ending]:
                if ending != "None":
                    finalEnd = int(ending)
                else:
                    finalEnd = None

        if finalEnd and finalMiddle:
            reps.append([finalStart, finalMiddle, finalEnd])

    return reps

def getCloser(cycles, keyFrames, anglesInkeyframes, model : Workout):

    reps = []

    maxLen = 0
    for joint in cycles:
        for cycleJoint in joint:
            if cycleJoint[3] < 5: #remove cycles under 5 degrees
                joint.remove(cycleJoint)
            
                
        if len(joint) > maxLen:
            maxLen = len(joint)
    

    potentialReps = [[] for i in range(maxLen)]


    for joint in  cycles:
        n = 0
        for cycleJoint in joint:
            potentialReps[n].append(cycleJoint)
            n = n + 1
    
    for cycleGroup in potentialReps: #Take the best values
        lastEnd = 0
        starts = {}
        middle = {}
        end = {} 
        for cycle in cycleGroup:
            
            if str(cycle[0]) in starts.keys():
                starts[str(cycle[0])] = starts[str(cycle[0])] + 1
            else:
                starts[str(cycle[0])] = 1

            if str(cycle[1]) in middle.keys():
                middle[str(cycle[1])] = middle[str(cycle[1])] + 1
            else:
                middle[str(cycle[1])] = 1

            if str(cycle[2]) in end.keys():
                end[str(cycle[2])] = end[str(cycle[2])] + 1
            else:
                end[str(cycle[2])] = 1
            print(starts)
        finalStart = 0
        finalMiddle = 1
        finalEnd = 2
        for start in starts.keys():#TODO Use standard deviation comparasion to not skip reps
            if not finalStart or (model.compareToTop(WorkoutPose(anglesInkeyframes[keyFrames[int(start)][1]]))\
                                        < \
                                  model.compareToTop(WorkoutPose(anglesInkeyframes[keyFrames[int(finalStart)][1]]))):
               #if difference to the model is less than what we have 
                if int(start) >= lastEnd:
                    finalStart = int(start)

        for mid in middle.keys():
            if mid == "None":
                finalMiddle = None
            elif not finalMiddle or (model.compareToBottom(WorkoutPose(anglesInkeyframes[keyFrames[int(mid)][1]]))\
                                        < \
                                   model.compareToBottom(WorkoutPose(anglesInkeyframes[keyFrames[int(finalMiddle)][1]]))):
                if int(mid) > lastEnd:
                    finalMiddle = int(mid)
                

        for ending in end.keys():
            if ending == "None":
                finalEnd = None
            elif not finalEnd or (model.compareToTop(WorkoutPose(anglesInkeyframes[keyFrames[int(ending)][1]]))\
                                        < \
                                model.compareToTop(WorkoutPose(anglesInkeyframes[keyFrames[int(finalEnd)][1]]))):
                if int(ending) > lastEnd:
                    finalEnd = int(ending)

        reps.append([finalStart, finalMiddle, finalEnd])
        lastEnd = finalEnd

    return reps

def setupNewWorkout():
    
    models = os.listdir("ComputerVisionTest/models")
    print(models)
    name = input("Name of new workout: ").strip()
    while (len(name) == 0) and (name + ".json") in models:

        name = input("Model already exists or the name is invalid! \n\
Please provide a new name of new workout: ").strip()

    print(MENU)
    choices = input("Choice(s): ").split(",")

    return name, choices

def get_average(data):
    return mean(data)


def get_standard_deviation(data):
    return statistics.stdev(data)


def makeNewModelV1(extracted, allAngles):
    keypointAngles = []

    for frame in extracted:
        keypointAngles.append(allAngles[frame[1]])

    reps, modelName, importantAngles = getReps(extracted, allAngles)
    print(f"Reps: {reps}")
    model = {}
    listOfTop = []
    listOfBottom = []
    
    for i in range(len(reps)):
        rep = reps[i]
        listOfTop.append(keypointAngles[rep[0]]) 
        listOfBottom.append(keypointAngles[rep[1]])
        listOfTop.append(keypointAngles[rep[2]])
    
    listOfTop = KeyframeExtraction.simplifiedCurveModel(listOfTop)
    listOfBottom = KeyframeExtraction.simplifiedCurveModel(listOfBottom)
            

    averageTop, StdevOfTop = getAverageAndStdvOfList(listOfTop)
    averageBottom, StdevOfBottom = getAverageAndStdvOfList(listOfBottom)

    model["Top"] = [averageTop, StdevOfTop, len(listOfTop[0])*2]
    model["Bottom"] = [averageBottom, StdevOfBottom, len(listOfBottom[0])]
    model["ImportantAngles"] = importantAngles
    path = "ComputerVisionTest/models/" + modelName + ".json"
    with open(path, 'w') as f:
        json.dump(model, f)

    return model

def getAverageAndStdvOfList(list):
    averages = []
    stdvs = []
    for i in range(len(list)):
        print(f"list[{i}] = {list[i]}")
        averages.append(get_average(list[i]))
        stdvs.append(get_standard_deviation(list[i]))
    
    return averages, stdvs

def updateModelV1(videoPath, modelName):
    extracted, allAngles = getKeyFramesFromVideo(videoPath)
    keypointAngles = []

    for frame in extracted:
        keypointAngles.append(allAngles[frame[1]])

    reps, modelName, importantAngles = getReps(extracted, allAngles, modelName)
    print(f"Reps: {reps}")
    path = f"ComputerVisionTest/models/{modelName}.json"
    model = Workout().loadModel(f"ComputerVisionTest/models/{modelName}.json")
    
    for rep in reps:
        model.updateModel(WorkoutPose(keypointAngles[rep[0]]), "Top")
        model.updateModel(WorkoutPose(keypointAngles[rep[2]]), "Top")
        model.updateModel(WorkoutPose(keypointAngles[rep[1]]), "Bottom")

    model.saveModel(path)
    return model

def demo1():

    print("Analyzing video 1...")
    extracted, allAngles = getKeyFramesFromVideo("ComputerVisionTest/videos/Pushupangleview.mp4")

    model = makeNewModelV1(extracted, allAngles)
    n = input("Frame to display: ")
    while n != "no":
    
        n = int(n)
        mp_drawing_modified.plot_landmarks(extracted[n][0].pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
        n = input("Frame to display: ")

    print("Analyzing video 2...")
    updateModelV1("ComputerVisionTest/videos/pushup.mp4", "pushups")

if __name__ == "__main__":
    #demo1()
    MENU2 = "Choices:\n1. Create New Model\n2. Train Existing Model\n3. Quit\nChoice: "
    choice = input(MENU2)
    while choice != "1" and choice != "2" and choice != "3":
        print("Wrong Input!")
        choice = input(MENU2)

    while choice != "3":
        if choice == "1":
            video = input("Path to video: ")
            extracted, allAngles = getKeyFramesFromVideo(video)
            model = makeNewModelV1(extracted, allAngles)
            print(f"New workout added\n")
        
        elif choice == "2":
            name = input("Workout name: ")
            video = input("Path to video: ")
            updateModelV1(video, name)
            print(f"{name} updated\n")

        MENU2 = "Choices:\n1. Create New Model\n2. Train Existing Model\n3. Quit\nChoice: "
        choice = input(MENU2)
        while choice != "1" and choice != "2" and choice != "3":
            print("Wrong Input!")
            choice = input(MENU2)
        