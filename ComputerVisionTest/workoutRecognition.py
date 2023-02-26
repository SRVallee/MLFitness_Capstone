'''

'''
import cv2
import mediapipe as mp
import numpy as np
import math
import json
import statistics
import os
from pathlib import Path
import binomialFitting.KeyframeExtraction as KeyframeExtraction
import machineLearning.MachineLearningInitial as mli
import mp_drawing_modified
from Workout import Workout
from WorkoutPose import WorkoutPose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

#body angle 
MENU = "Select the joints that cycle separated by commas \n\
    Ex. for push ups: 4,5\n\n\
1   head angle \n\
2   body angle\n\
3   left shoulder\n\
4   left hip\n\
5   right shoulder\n\
6   right hip\n\
7   left elbow\n\
8   left knee\n\
9   right elbow\n\
10  right knee"

choiceList = {
    "1":    [0,1],
    "2":    [2,3],
    "3":    [4,5],
    "4":    [6,7],
    "5":    [8,9],
    "6":    [10,11],
    "7":    [12],
    "8":    [13],
    "9":    [14],
    "10":   [15]
}

def getJoint(angle):
    a = int(angle)
    if a in range(12):
        return a//2 +1
    else:
        return a - 5

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
    frameTime = 0
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
                frameTime = 5
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
            if cv2.waitKey(frameTime) & 0xFF == 27:
                break

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    #print(f"frames: {len(allFrames)}")
    #print(f"framerate: {fps}")

    rSquared = 0.5

    print(f"RSquared: {rSquared}")
    #extracted is a list of tuples with class Solution outputs and the actual frame
    extracted, allangles, keyAngs = KeyframeExtraction.extractFrames(allFrames, rSquared, True)
    print(f"{len(extracted)} frames extracted")
    return extracted, allangles, keyAngs


def getReps(keyFrames, anglesPerFrame, repNumber = None, workout = None, increaseGiven = True):
    allAngles = KeyframeExtraction.simplifiedCurveModel(anglesPerFrame)
    if not workout:
        modelName, importantJoints, repNumber = setupNewWorkout()
        importantAngles = convertJoints(importantJoints)
    else:
        modelName = workout
        model = Workout().loadModel(f"ComputerVisionTest/models/{workout}.json")
        importantAngles = model.getImportantAngles()
    nFrames = len(keyFrames)
    reptypes = [[] for i in range(nFrames)] 
    cycles = [[] for i in range(len(importantAngles))] #[start, turning point, end, angle]

    for curve in range(len(importantAngles)): #Only include important Joint angles
        angle1, angle2, increase = None, None, None
        
        #get cycles
        for frame in range(nFrames):

            angle1 = angle2
            angle2 = allAngles[importantAngles[curve]][keyFrames[frame][1]] #all angles includes all Frames, not just keyframes

            if(angle1 != 0 and not angle1): #if first angle
                angle1 = angle2

            else: #get direction change and angle difference
                #if last frame was a decrease and now it's increasing
                if (angle1 < angle2) and increase == False: #can be None
                    increase = True
                    reptypes[frame].append([angle2, curve, increase, angle2 - angle1])

                    if not increaseGiven:
                        cycles[curve][-1][2] = frame #TODO comment this what is this why is it subtracting
                        if cycles[curve][-1][3] < (angle2 - angle1): #a list within a list witin a list
                            cycles[curve][-1][3] = angle2 - angle1
                        cycles[curve].append([frame, None, None, angle2 - angle1])
                    else:
                        cycles[curve][-1][1] = frame
                        if cycles[curve][-1][3] < (angle2 - angle1):
                            cycles[curve][-1][3] = angle2 - angle1

                    angle1 = angle2

                #if last frame was an increase and now it's a decrease
                elif (angle1 > angle2) and increase:
                    increase = False
                    reptypes[frame].append([angle2, curve, increase, angle1 - angle2])
                    
                    if increaseGiven:
                        cycles[curve][-1][2] = frame
                        if cycles[curve][-1][3] < (angle1 - angle2):
                            cycles[curve][-1][3] = angle1 - angle2
                        cycles[curve].append([frame, None, None, angle1 - angle2])
                    else:
                        cycles[curve][-1][1] = frame
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

                        angle1 = angle2

                    
                    else:
                        increase = False
                        reptypes[frame].append([angle2, curve, increase, angle1 - angle2])
                        reptypes[0].append([angle1, curve, True, 0])
                        cycles[curve].append([0, frame, None, angle1 - angle2]) #Set Values for first time setup.
                        angle1 = angle2
                    
    #check important joint changes
    i = 1

    allCycles = cycles[0] + cycles[1]  #TODO Include more angles!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    #get reps without model
    if not workout:
        parallel = getTrend(allCycles, int(repNumber))
    else:
        if repNumber:
            parallel = getCloser(allCycles, keyFrames, anglesPerFrame, model, int(repNumber))
        else:
            parallel = getCloser(allCycles, keyFrames, anglesPerFrame, model)

    #print(f"cycles: {parallel}")

    for cycle in parallel:
        if not cycle[1]:
            parallel.remove(cycle)
        elif not cycle[2]:
            cycle[2] = len(keyFrames)-1
    print(f"important Angles from get rep {importantAngles}")
    return parallel, modelName, importantAngles

def getTrend(cycles, repNumber = 9999):
    #cycle [start, turning point, end, angle]

    reps = []


    for cycleJoint in cycles:
        
        if cycleJoint[3] < math.radians(10): #remove cycles under 5 degrees
            cycles.remove(cycleJoint)

    
    pairs = getPairs(cycles)
    pairList = []
    for pair in pairs:
        pairList.append(cycles[pair[0]])

    if len(pairList) == repNumber:
        return pairList 
        
    #print(f"pairlist: {pairList}")
    for cycle in cycles:
        if cycle in pairList:
            cycles.remove(cycle)
    #print(f"pairlist: {pairList}")
    reps = pairList
    for cycle in cycles:
        #print(f"cycle: {cycle}")
        if len(reps) < repNumber and checkValidRange(cycle, reps):
            reps = insertRep(reps, cycle)
            #print(f"reps: {reps}")

    return reps

def insertRep(reps, rep): #assums rep is valid

    if len(reps) == 0:
        reps.append(rep)
        return reps

    for i in range(len(reps)):

        if rep[2] <= reps[i][0]:
            reps.insert(i, rep)
            return reps

        elif i == len(reps) -1:
            reps.append(rep)
            return reps
        

def checkValidRange(cycle, reps):
    if None in cycle:
        return False

    for rep in reps:
        if rep[0] <= cycle[0] and rep[2] > cycle[0]:
            return False
        elif rep[0] < cycle[2] and rep[2] >= cycle[2]:
            return False

    return True




def getPairs(cycles):
    pairs = []
    visited = []
    for j in range(len(cycles)):
        cycle = cycles[j]
        for i in range(len(cycles)):
            pair = cycles[i]
            if cycle[0] == pair[0]\
           and cycle[1] == pair[1]\
           and cycle[2] == pair[2]\
           and i != j:
                if not j in visited:
                    pairs.append((j,i))
                    visited.append(j)
                    visited.append(i)

    return pairs

#getCloser
#checks if keyframe before and current keyframe are a larger difference than 10 degrees
#if so than append it as a rep if not removes from keyframe list
#
#parameters: cycles()
#
#
def getCloser(cycles, keyFrames, anglesInkeyframes, model : Workout, repNumber:int = 9999):

    reps = []

    for cycleJoint in cycles:
        
        if cycleJoint[3] < math.radians(10): #remove cycles under 10 degrees
            cycles.remove(cycleJoint)
    
    #print(cycles)        

    pairs = getPairs(cycles)
    pairList = []
    for pair in pairs:
        pairList.append(cycles[pair[0]])

    if len(pairList) == repNumber:
        return pairList 
    
    for cycle in cycles:  #Temporary until I fixed commented code
        if cycle in pairList:
            cycles.remove(cycle)

    reps = pairList
    
    for cycle in cycles:
        if len(reps) < repNumber and checkValidRange(cycle, reps):
            reps = insertRep(reps, cycle)


    # for joint in  cycles:
    #     n = 0
    #     for cycleJoint in joint:
    #         potentialReps[n].append(cycleJoint)
    #         n = n + 1
    
    # for cycleGroup in potentialReps: #Take the best values
    #     lastEnd = 0
    #     starts = {}
    #     middle = {}
    #     end = {} 
    #     for cycle in cycleGroup:
            
    #         if str(cycle[0]) in starts.keys():
    #             starts[str(cycle[0])] = starts[str(cycle[0])] + 1
    #         else:
    #             starts[str(cycle[0])] = 1

    #         if str(cycle[1]) in middle.keys():
    #             middle[str(cycle[1])] = middle[str(cycle[1])] + 1
    #         else:
    #             middle[str(cycle[1])] = 1

    #         if str(cycle[2]) in end.keys():
    #             end[str(cycle[2])] = end[str(cycle[2])] + 1
    #         else:
    #             end[str(cycle[2])] = 1
    #         #print(starts)
    #     finalStart = None
    #     finalMiddle = None
    #     finalEnd = None
    #     for start in starts.keys():#TODO Use standard deviation comparasion to not skip reps
    #         if not finalStart or (model.compareToTop(WorkoutPose(anglesInkeyframes[keyFrames[int(start)][1]]))\
    #                                     < \
    #                               model.compareToTop(WorkoutPose(anglesInkeyframes[keyFrames[int(finalStart)][1]]))):
    #            #if difference to the model is less than what we have 
    #             if int(start) >= lastEnd:
    #                 finalStart = int(start)
    #                 lastEnd = int(start)

    #     for mid in middle.keys():
    #         if mid == "None":
    #             finalMiddle = None
    #         elif not finalMiddle or (model.compareToBottom(WorkoutPose(anglesInkeyframes[keyFrames[int(mid)][1]]))\
    #                                     <= \
    #                                model.compareToBottom(WorkoutPose(anglesInkeyframes[keyFrames[int(finalMiddle)][1]]))):
    #             if int(mid) > lastEnd:
    #                 finalMiddle = int(mid)
    #                 lastEnd = int(mid)
                

    #     for ending in end.keys():
    #         if ending == "None":
    #             finalEnd = None
    #         elif not finalEnd or (model.compareToTop(WorkoutPose(anglesInkeyframes[keyFrames[int(ending)][1]]))\
    #                                     <= \
    #                             model.compareToTop(WorkoutPose(anglesInkeyframes[keyFrames[int(finalEnd)][1]]))):
    #             if int(ending) > lastEnd:
    #                 finalEnd = int(ending)
    #                 lastEnd = int(ending)

    #     reps.append([finalStart, finalMiddle, finalEnd])
    #     lastEnd = finalEnd

    return reps

def setupNewWorkout():
    
    models = os.listdir("ComputerVisionTest/models")
    print(models)
    name = input("Name of new workout: ").strip()
    reps = input("number of repetitions: ")
    while (len(name) == 0) and (name + ".json") in models:

        name = input("Model already exists or the name is invalid! \n\
Please provide a new name of new workout: ").strip()

    print(MENU)
    choices = input("Choice(s): ").split(",")

    return name, choices, reps

def get_average(data):
    return mean(data)


def get_standard_deviation(data):
    return statistics.stdev(data)

def getRepsFromVideo(videoPath, modelName):
    extracted, allAngles = getKeyFramesFromVideo(videoPath)
    keypointAngles = []

    for frame in extracted:
        keypointAngles.append(allAngles[frame[1]])

    return getReps(extracted, allAngles, modelName)


def makeNewModelV1(extracted, allAngles, debug = False):
    keypointAngles = []

    for frame in extracted:
        keypointAngles.append(allAngles[frame[1]])

    reps, modelName, importantAngles = getReps(extracted, allAngles)
    #print(f"Reps: {reps}")
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
    print(f"Sdv returned: {StdevOfBottom}")

    model["Top"] = [averageTop, StdevOfTop, len(listOfTop[0])*2]
    model["Bottom"] = [averageBottom, StdevOfBottom, len(listOfBottom[0])]
    model["ImportantAngles"] = importantAngles
    path = "ComputerVisionTest/models/" + modelName + ".json"
    with open(path, 'w') as f:
        json.dump(model, f)

    if debug:
        n = input("Frame to display: ")
        while n != "no":
  
            n = int(n)-1
            mp_drawing_modified.plot_landmarks(extracted[n][0].pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
            n = input("Frame to display: ")

    return model

def getAverageAndStdvOfList(list):
    averages = []
    stdvs = []
    for i in range(len(list)):
        averages.append(get_average(list[i]))
        stdvs.append(get_standard_deviation(list[i]))
    
    return averages, stdvs

def updateModelV1(videoPath, modelName, repNumber, debug = False):
    extracted, allAngles, importangles = getKeyFramesFromVideo(videoPath)
    keypointAngles = []

    for frame in extracted:
        keypointAngles.append(allAngles[frame[1]])

    reps, modelName, importantAngles = getReps(extracted, allAngles, repNumber, modelName)
    #print(f"Reps: {reps}")
    path = f"ComputerVisionTest/models/{modelName}.json"
    model = Workout().loadModel(f"ComputerVisionTest/models/{modelName}.json")
    
    for rep in reps:
        if not None in rep:
            model.updateModel(WorkoutPose(keypointAngles[rep[0]]), "Top")
            model.updateModel(WorkoutPose(keypointAngles[rep[2]]), "Top")
            model.updateModel(WorkoutPose(keypointAngles[rep[1]]), "Bottom")

    if debug:
        n = input("Frame to display: ")
        while n != "no":
  
            n = int(n)-1
            mp_drawing_modified.plot_landmarks(extracted[n][0].pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
            n = input("Frame to display: ")

    model.saveModel(path)
    return model


def evaluateVideo(videoPath, modelName, repNumber, debug = None):
    extracted, allAngles,impotantangs = getKeyFramesFromVideo(videoPath)
    keypointAngles = []

    for frame in extracted:
        keypointAngles.append(allAngles[frame[1]])

    reps, modelName, importantAngles = getReps(extracted, allAngles, repNumber, modelName)
    path = f"ComputerVisionTest/models/{modelName}.json"
    model = Workout().loadModel(f"ComputerVisionTest/models/{modelName}.json")
    right = []
    wrong = []
    for rep in reps:
        pose1, pose2, pose3 = model.validateWorkout(WorkoutPose(keypointAngles[rep[0]]), WorkoutPose(keypointAngles[rep[1]]), WorkoutPose(keypointAngles[rep[2]]))
        if pose1 == 0:
            wrong.append(rep[0])
        else:
            right.append(rep[0])

        if pose2 == 0:
            wrong.append(rep[1])
        else:
            right.append(rep[1])

        if pose3 == 0:
            wrong.append(rep[2])
        else:
            right.append(rep[2])

    if debug:
        print(f"Right Reps: {right}")
        print(f"wrong Reps: {wrong}")
        n = input("Frame to display: ")
        
        while n != "no":
  
            n = int(n)-1
            mp_drawing_modified.plot_landmarks(extracted[n][0].pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
            n = input("Frame to display: ")
    

    return right, wrong


def trainML(modelName):
    vidsDir = Path.cwd().parents[0]
    # paths = [vidsDir + "\\vids\\good_trainML\\", # good reps folder
    #          vidsDir + "\\vids\\bad_trainML\\"] # bad reps folder
    paths = [str(vidsDir) + "\\ML_training\\correct_trainML\\angle_squat\\", # good reps folder
             str(vidsDir) + "\\ML_training\\incorrect_trainML\\angle_squat\\"] # bad reps folder
    allReps = []
    totalAngles = []
    lengths = [] # lengths of good reps, bad reps
    for path in paths: #first good paths, then bad paths
        for filename in os.listdir(path):
            videoPath = path + filename
            extracted, allAngles, keyAngs = getKeyFramesFromVideo(videoPath)
            totalAngles.append(keyAngs)
            reps, modelName, importantAngles = getReps(extracted, allAngles, workout=modelName)
            allReps.append(reps)
            
        if len(lengths) < 1:
            lengths.append(len(allReps))
        else:
            lengths.append(len(allReps) - lengths[0])
            
    df = mli.repsToDataframe(allReps, totalAngles, lengths)
    
    return mli.do_ml(df, importantAngles)

# This function will grab video path from user and what model it is for key extraction
# and the trained model to evaluate the video if the reps are correct or not
#
#
#
#
def vid_ML_eval(modelName,trained_MLmodel, vid_path):
    totalAngles = []
    extracted, allAngles, keyAngs = getKeyFramesFromVideo(vid_path)
    totalAngles.append(keyAngs)
    reps, modelName, importantAngles = getReps(extracted, allAngles, workout=modelName)
    print(f"amount of reps: {reps}")
    df =mli.dataframeforeval(reps, allAngles)
    mli.vid_ml_eval(trained_MLmodel, df, extracted, reps)
    return True

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
    MENU2 = """
    Choices:
    1. Create New Rep Model
    2. Update Existing Rep Model
    3. Evaluate Video
    4. Train and Test Machine Learning Analysis 
    5. Machine learning video input
    6. Quit\nChoice: """
    model_created = 0
    while True:
        choice = input(MENU2)
        if choice == "1":
            video = input("Path to video: ").strip("'")
            extracted, allAngles,impangs = getKeyFramesFromVideo(video)
            model = makeNewModelV1(extracted, allAngles, True)
            print(f"New workout added\n")
        
        elif choice == "2":
            name = input("Workout name: ")
            #numberOfReps = input("Number of reps: ")
            video = input("Path to video: ").strip("'")
            updateModelV1(video, name, True)
            print(f"{name} updated\n")
            
        elif choice == "3":
            name = input("Workout name: ")
            numberOfReps = input("Number of reps: ")
            video = input("Path to video: ").strip("'")
            right, wrong = evaluateVideo(video, name, numberOfReps, True)
        
        elif choice == "4":
            name = input("Workout name: ")
            trained_model = trainML(name)
            model_created = 1
            
        elif choice == "5" and model_created == 1:
            name = input("workout name: ")
            path = input("video path: ")
            vid_ML_eval(name,trained_model, path)
            #mli.vid_ml_eval(name, path)
            
        elif choice == "5" and model_created == 0:
            print("Error No trained model")
            print("choice 4 of training model has not yet been made")
            
        elif choice == "6" or choice == "q":
            break
            
        else:
            print("Incorrect input, try again.")
            continue

        