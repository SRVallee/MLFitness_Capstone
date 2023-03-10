'''

'''
import cv2
import tensorflow as tf
import mediapipe as mp
import math
import json
import statistics
import os
from pathlib import Path
import binomialFitting.KeyframeExtraction as KeyframeExtraction
import machineLearning.MachineLearningInitial as mli
import evalPoseDisplay as poseDisplay
from Workout import Workout
from WorkoutPose import WorkoutPose
import multiprocessing as mproc
import pandas as pd

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

from statistics import mean
from statistics import stdev

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

def getParallelJoint(joint):
    if joint == 3:
        return choiceList["5"]
    elif joint == 5:
        return choiceList["3"]
    elif joint == 4:
        return choiceList["6"]
    elif joint == 6:
        return choiceList["4"]
    elif joint == 7:
        return choiceList["9"]
    elif joint == 9:
        return choiceList["7"]
    elif joint == 8:
        return choiceList["10"]
    elif joint == 10:
        return choiceList["9"]


####### STATS #######
def get_average(data):
    return mean(data)


def get_standard_deviation(data):
    return statistics.stdev(data)


def getAverageAndStdvOfList(list):
    averages = []
    stdvs = []
    for i in range(len(list)):
        averages.append(get_average(list[i]))
        stdvs.append(get_standard_deviation(list[i]))

    return averages, stdvs

# REP COMPUTATION
def getKeyFramesFromVideo(video, show = False):
    cap = cv2.VideoCapture(video)
    allFrames = []
    frameTime = 0
    with mp_pose.Pose(static_image_mode=False,
               model_complexity=2,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
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


# TODO: EXPLAIN THIS
def getReps(keyFrames, anglesPerFrame, repNumber = None, workout = None, increaseGiven = True):
    allAngles = KeyframeExtraction.simplifiedCurveModel(anglesPerFrame)
    if not workout:
        modelName, importantJoints, excludeJoints = setupNewWorkout()
        importantAngles = convertJoints(importantJoints)
        excludeAngles = convertJoints(excludeJoints)
    else:
        modelName = workout
        modelDir = str(os.path.dirname(__file__))
        path = f"{str(modelDir)}\\models\\"
        model = Workout().loadModel(f"{path}{workout}.json")
        importantAngles = model.getImportantAngles()
        excludeAngles = model.getExcludeAngles()
        
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
                        if cycles[curve][-1][3] < (angle2 - angle1): #a list within a list within a list
                            cycles[curve][-1][3] = angle2 - angle1
                        cycles[curve].append([frame, None, None, angle2 - angle1, importantAngles[curve]])
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
                        cycles[curve].append([frame, None, None, angle1 - angle2, importantAngles[curve]])
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
                        cycles[curve].append([0, frame, None, angle2 - angle1, importantAngles[curve]]) #Set Values for first time setup.

                        angle1 = angle2

                    
                    else:
                        increase = False
                        reptypes[frame].append([angle2, curve, increase, angle1 - angle2])
                        reptypes[0].append([angle1, curve, True, 0])
                        cycles[curve].append([0, frame, None, angle1 - angle2, importantAngles[curve]]) #Set Values for first time setup.
                        angle1 = angle2
                    
    #check important joint changes
    i = 1

    allCycles = cycles[0] + cycles[1]  #TODO Include more angles!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    anglesFromExtracted = []
    for frame in keyFrames:
        anglesFromExtracted.append(anglesPerFrame[frame[1]])

    for cycle in allCycles:
        if not cycle[1]:
            allCycles.remove(cycle)
        elif not cycle[2]:
            cycle[2] = len(keyFrames)-1


    #get reps without model           #Not using getCloser for now
    #if not workout:
    if not repNumber:
        parallel = getTrend(allCycles, anglesFromExtracted)
    else:
        parallel = getTrend(allCycles, anglesFromExtracted, int(repNumber))
        

    #print(f"cycles: {parallel}")

    return parallel, modelName, importantAngles, excludeAngles


# TODO EXPLAIN THIS
def getTrend(cycles, allAngles, repNumber = 9999):
    #cycle [start, turning point, end, angle]

    reps = []

    for cycleJoint in cycles:
        
        if cycleJoint[3] < math.radians(5): #remove cycles under 5 degrees
            cycles.remove(cycleJoint)

    #print(f"all cycles before pairs: {cycles}")
    pairs = getPairs(cycles)
    pairList = []
    for pair in pairs:
        pairList.append(cycles[pair[0]])

    if len(pairList) == repNumber:
        return pairList 
        
    for cycle in cycles:
        if cycle in pairList:
            cycles.remove(cycle)
    #print(f"pairlist: {pairList}")
    
    reps = pairList

    for i in range(len(cycles)):
        cycle = pickLargest(cycles)
        parallelAngle = getParallelCycleAngle(cycle, allAngles)
        cycles.remove(cycle)
        if parallelAngle and parallelAngle > math.radians(5): 
        
            if len(reps) < repNumber and checkValidRange(cycle, reps):
                reps = insertRep(reps, cycle)
    
    return reps


# TODO EXPLAIN THIS
def getParallelCycleAngle(cycle, allAngles):
    if not cycle[0] or not cycle[1] or not cycle[2]:
        return
    opositeAngles = getParallelJoint(getJoint(cycle[4]))
    #print(f"\ncycle: {cycle}")
    #print(f"Oposite angles: {opositeAngles}")
    maxAngles = []
    if opositeAngles:
        for angle in opositeAngles:
            #print(f"allAngleslen: {len(allAngles)}")
            #print(f"framelen: {len(allAngles[0])}")
            angle1 = abs(allAngles[cycle[0]][angle] - allAngles[cycle[1]][angle])
            angle2 = abs(allAngles[cycle[1]][angle] - allAngles[cycle[2]][angle])
            if angle1 > angle2:
                maxAngles.append(angle1)
            else:
                maxAngles.append(angle2)
    #print(f"\nmax angles: {maxAngles}")

    if maxAngles:
        #print(f"returning: {max(maxAngles)}")
        return max(maxAngles)
    return


# TODO EXPLAIN THIS
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
        

# TODO EXPLAIN THIS
def checkValidRange(cycle, reps):
    if None in cycle:
        return False

    for rep in reps:
        if rep[0] <= cycle[0] and rep[2] > cycle[0]:
            return False
        elif rep[0] < cycle[2] and rep[2] >= cycle[2]:
            return False

    return True


# TODO EXPLAIN THIS
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
           and cycle[3] > math.radians(10)\
           and pair[3] > math.radians(10)\
           and i != j:
                if not j in visited:
                    pairs.append((j,i))
                    visited.append(j)
                    visited.append(i)

    return pairs


# TODO EXPLAIN THIS
def pickLargest(cycles):
    largest = [0,0,0,0]
    for cycle in cycles:
        if cycle[3] > largest[3]:
            largest = cycle
    if largest != [0,0,0,0]:
        return largest


# Set up a new workout
def setupNewWorkout():
    modelDir = str(os.path.dirname(__file__)) #MLFITNESS_Capstone
    models = str(modelDir) + "\\models\\"
    print(models)
    name = input("Name of new workout: ").strip()
    while (len(name) == 0) and (name + ".json") in models:

        name = input("Model already exists or the name is invalid! \n\
Please provide a new name of new workout: ").strip()

    print(MENU)
    importantAngs = input("Choice(s): ").split(",")

    print("Please enter joints to exclude")
    print(MENU)
    excludeAngs = input("Choice(s): ").split(",")

    return name, importantAngs, excludeAngs


# TODO ???????
def getRepsFromVideo(videoPath, modelName):
    extracted, allAngles = getKeyFramesFromVideo(videoPath)
    keypointAngles = []

    for frame in extracted:
        keypointAngles.append(allAngles[frame[1]])

    return getReps(extracted, allAngles, modelName)


# TODO ??????????
def makeNewModelV2():
    #print(f"Reps: {reps}")
    model = {}
    modelName, importantJoints, excludeJoints = setupNewWorkout()
    importantAngles = convertJoints(importantJoints)
    excludeAngles = convertJoints(excludeJoints)
    model["ImportantAngles"] = importantAngles
    model["ExcludeAngles"] = excludeAngles
    modelDir = str(os.path.dirname(__file__)) #MLFITNESS_Capstone
    models = str(modelDir) + "\\models\\"
    path = models + modelName + ".json"
    with open(path, 'w') as f:
        json.dump(model, f)

    return model


# Compute a dataframe from the provided videos and then save it
def computeData(modelName):
    vidsDir = Path.cwd().parents[0]
    # paths = [vidsDir + "\\vids\\good_trainML\\", # good reps folder
    #          vidsDir + "\\vids\\bad_trainML\\"] # bad reps folder
    paths = [str(vidsDir) + "\\ML_training\\correct_trainML\\angle_squat\\", # good reps folder
             str(vidsDir) + "\\ML_training\\incorrect_trainML\\angle_squat\\"] # bad reps folder
    #put threads or mulitprocessing here
    
    lengths = 1 # lengths of good reps
    frames =[]
    for path in paths: #first good paths, then bad paths
        items = []
        allReps = []
        totalAngles = []
        for filename in os.listdir(path):
            args = (path, filename, modelName)
            items.append(args)
        print(f"items(path, filename, modelName): {len(items)}")
        with mproc.Pool() as pool:
            results = pool.map(process_divider, items)
            print(f"results: {len(results)}")
            for all_items in results:
                importantAngles, allReps_vids, totalAngles_vid, excludeAngs = all_items
                #print(f"importantAngles: {importantAngles}, allReps_vid: {allReps_vid}, totalAngles_vid: {totalAngles_vid}")
                print(f"this is all reps vids no append: {allReps_vids}")
                allReps.append(allReps_vids)#list of reps per vid
                totalAngles.append(totalAngles_vid)
        print(f"this is all reps: {allReps}. length is {len(allReps)}")
        print(f"this is all angles no append: {totalAngles}")
        print(f"\ntotalAngles: {len(totalAngles)}\n")
        print(f"\nallreps: {len(allReps)}. aprox total = {len(items)*5}\n")
        
        df = mli.repsToDataframe(allReps, totalAngles, lengths, excludeAngs)
        shaper = tf.shape(df)
        print(f"\nthis is df.shape before merge: {shaper}\n")
        #print(f"\nthis is df before merge: {df}\n")
        frames.append(df)
        lengths = 0
        pool.close()
        pool.join()
        items = []
        allReps = []
        totalAngles = []
        
    merged_df = pd.concat(frames)
    print(f"this is the merged df: {merged_df}")
    
    filename = str(os.path.dirname(__file__)) + "\\dataframes\\" + modelName + ".csv"
    merged_df.to_csv(filename, index=False)
    return merged_df


# Multi-Processing function
def process_divider(items):
    path, filename, modelName = items
    videoPath = path + filename
    extracted, allAngles, _ = getKeyFramesFromVideo(videoPath)
    
    keyAngs = []
    for frame in extracted:
        keyAngs.append(allAngles[frame[1]])
    
    reps, modelName, importantAngles, excludeAngles = getReps(extracted, allAngles, workout=modelName)
    print(f"this is filename: {filename}. this is the current reps: {reps}")
    return importantAngles, reps, keyAngs, excludeAngles


# Open or create a dataframe and the 
def open_and_train(modelName):
    cwd = cwd = str(os.path.dirname(__file__))
    dataName = str(cwd) + "/dataframes/" + modelName + ".csv"
    path = f"{str(cwd)}\\models\\"
    model = Workout().loadModel(f"{path}{modelName}.json")
    importantAngles = model.getImportantAngles()
    
    if os.path.isfile(dataName): # if dataframe exists, open
        df = pd.read_csv(dataName)
        
    else:                        # else create a dataframe and save it
        df = computeData(modelName)
        
    return mli.do_ml(df, importantAngles, modelName)


# This function will grab video path from user and what model it is for key extraction
# and the trained model to evaluate the video if the reps are correct or not
#
def vid_ML_eval(modelName,trained_MLmodel, vid_path):

    extracted, allAngles, _ = getKeyFramesFromVideo(vid_path)
    keyAngs = []
    for frame in extracted:
        keyAngs.append(allAngles[frame[1]])
    
    reps, modelName, importantAngles, exclude_angles = getReps(extracted, allAngles, workout=modelName)
    df =mli.dataframeforeval(reps, keyAngs, exclude_angles)
    print(f"these are excluded values: {exclude_angles}\n the df with excluding angles: {df}")
    print(f"amount of reps: {reps}")
    rep_list, frame_rep_list= mli.vid_ml_eval(modelName,trained_MLmodel, df, extracted, reps, importantAngles)
    print(f"extracted: {extracted}")
    return rep_list, extracted


if __name__ == "__main__":
    MENU2 = """
    Choices:
    1. Create New Rep Model
    2. Compute dataframe from videos
    3. Train,Test, and save Machine Learning Analysis 
    4. load existing Machine learning model for video input
    5. Quit\nChoice: """
    print(f"os.getcwd(): {os.getcwd()}")
    print(f"str(os.path.dirname(__file__)): {str(os.path.dirname(__file__))}")
    while True:
        choice = input(MENU2)
        if choice == "1":
            # video = input("Path to video: ").strip("'")
            # extracted, allAngles,impangs = getKeyFramesFromVideo(video)
            model = makeNewModelV2()
            print(f"New workout added\n")

        elif choice == "2":
            name = input("Workout name: ")
            computeData(name)
            
        elif choice == "3":
            name = input("Workout name: ")
            trained_model = open_and_train(name)

        elif choice == "4":
            name = input("workout name: ")
            path = input("video path: ")
            cwd = str(os.path.dirname(__file__))
            # try:
            model_path = str(cwd) + "\\ML_Trained_Models\\"+ str(name)+"_trained"
            load_model = tf.keras.models.load_model(model_path)
            acutal_frame_list, extracted =vid_ML_eval(name,load_model, path)
            print(f"actual_frame_list: {acutal_frame_list}\n\n extracted: {extracted}")
            n = 1
            all_frame_list = [x[n] for x in extracted]
            final_frame_list = []
            for i in range(0,len(all_frame_list),3):
                if len(all_frame_list[i:i+3]) == 3:
                    final_frame_list.append(all_frame_list[i:i+3])
            print(f"all_frame_list: {all_frame_list}")
            print(f"final_frame_list: {final_frame_list}")
            poseDisplay.capture_feed(path, final_frame_list)
            # except:
            #     print("\nModel name does not exist. create model using option 4")
            #     print("Models that exist are:")
            #     model_path = str(vidsDir) + "\\ML_Trained_Models\\"
            #     count = 1
            #     for filename in os.listdir(model_path):
            #         print(f"{count}: {filename}")
            #mli.vid_ml_eval(name, path)

        elif choice == "5" or choice == "q":
            break

        else:
            print("Incorrect input, try again.")
            continue
        