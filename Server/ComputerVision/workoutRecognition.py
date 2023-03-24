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
from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


from statistics import mean
from statistics import stdev

###### DEBUGGING VARIABLES ######
#this is for display original untocuhed video 
show_original_beginning_video = False

#this display every frame that key frame extraction returns
debug_Keyframe_extraction_vid = False

#this displays the actual rep frames to check if it is getting
#correct up and down frames
#in sets of 3
actual_rep_frame_display = False
##############################################################
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
#parameter: angle
#from menu seting up workout needs to have which angles are important
#out of 15 those that are chosen are than inputted into get joint, 
#parallel joints are stacked together like the 2 knees. 
# and returns the string number that corresponds with it
#Return: choice list  number
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
def getKeyFramesFromVideo(video):
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
            if show_original_beginning_video:

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

    

    #print(f"frames: {len(allFrames)}")
    #print(f"rep_frame_setsate: {fps}")


    rSquared = 0.5

    print(f"RSquared: {rSquared}, allframes len: {len(allFrames)}")
    #it literally halves the vid
    #extracted is a list of tuples with class Solution outputs and the actual frame
    extracted, allangles, keyAngs = KeyframeExtraction.extractFrames(allFrames, rSquared, True)
    
    #change var at top of file
    if debug_Keyframe_extraction_vid == True:
        constant_height = 700
        count = 1
        for tup in extracted:
            media, frame_num = tup
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            success, img = cap.read()
            height = img.shape[0]
            width = img.shape[1]
            height_percentage = float(constant_height/int(height))
            modded_width = int(float(width)*height_percentage)
            cv2.putText(img, f"keyframe extraction {count}, frame #: {frame_num}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            resize = cv2.resize(img, (modded_width, constant_height))
            cv2.imshow("Image", resize)
            count = count+1
            key = cv2.waitKey(0)  #millisecond delays
            if key == 27: #esc
                cv2.destroyWindow("Image")
    
    print(f"{len(extracted)} frames extracted")
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return extracted, allangles, keyAngs

# TODO: EXPLAIN THIS
#this functions gets all the changes in in angle direction and sends it to get trend
#also i believe that checking last frame is too small of variation to decide up and down
#how the code seems to work rn is that once the first frame of increase is detected that is top
def getReps(keyFrames, anglesPerFrame, repNumber = 9999, workout = None, increaseGiven = True):
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
    cycles = [[] for i in range(len(importantAngles))] #[start, turning point, end, angle]

    for curve in range(len(importantAngles)): #Only include important Joint angles
        angle1, angle2, increase = None, None, None
        
        #get cycles
        for frame in range(nFrames):

            angle1 = angle2
            #print(f"importantAngles[curve]: {importantAngles[curve]}, keyFrames[frame][1]: {keyFrames[frame][1]}")
            #print(f"allAngles[importantAngles[curve]][keyFrames[frame][1]]: {allAngles[importantAngles[curve]][keyFrames[frame][1]]}\n")
            angle2 = allAngles[importantAngles[curve]][keyFrames[frame][1]] #all angles includes all Frames, not just keyframes

            if(angle1 != 0 and not angle1): #if first angle
                angle1 = angle2

            else: #get direction change and angle difference
                #if last frame was a decrese and now it's increasing
                if (angle1 < angle2) and increase == False: #can be None
                    increase = True

                    if not increaseGiven:
                        #print(f"Top frame is last frame: {frame -1}, because last frame({frame-1}) angle : {angle1} > This frame({frame}): {angle2}")
                        cycles[curve][-1][2] = frame - 1
                        if cycles[curve][-1][3] < (angle2 - angle1):
                            cycles[curve][-1][3] = angle2 - angle1
                        cycles[curve].append([frame - 1, None, None, angle2 - angle1, importantAngles[curve]])
                    else:
                        #print(f"bottom frameis last frame: {frame-1}, because last frame({frame-1}) angle : {angle1} < This frame({frame}): {angle2}")
                        cycles[curve][-1][1] = frame - 1
                        if cycles[curve][-1][3] < (angle2 - angle1):
                            cycles[curve][-1][3] = angle2 - angle1

                    angle1 = angle2

                #if last frame was an increase and now it's a decrease
                elif (angle1 > angle2) and increase:
                    increase = False
                    
                    if increaseGiven:
                        #print(f"Top frame is last frame: {frame -1}, because last frame({frame-1}) angle : {angle1} > This frame({frame}): {angle2}")
                        cycles[curve][-1][2] = frame - 1
                        if cycles[curve][-1][3] < (angle1 - angle2):
                            cycles[curve][-1][3] = angle1 - angle2
                        cycles[curve].append([frame - 1, None, None, angle1 - angle2, importantAngles[curve]])
                    else:
                        #print(f"bottom frame is last frame: {frame -1}, because last frame({frame-1}) angle : {angle1} < This frame({frame}): {angle2}")
                        cycles[curve][-1][1] = frame -1
                        if cycles[curve][-1][3] < (angle1 - angle2):
                            cycles[curve][-1][3] = angle1 - angle2

                    angle1 = angle2

                #if comparing with first frame
                elif (increase == None):
                    
                    increase = not increaseGiven
                    cycles[curve].append([0, 0, 0, 0, importantAngles[curve]]) #Set Values for first time setup.

                    angle1 = angle2
                    
    allCycles = cycles[0] + cycles[1]  #TODO Include more angles!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    anglesFromExtracted = []
    for frame in keyFrames:
        anglesFromExtracted.append(anglesPerFrame[frame[1]])

    for cycle in allCycles:
        checkAngle = True
        if not cycle[1]:
            allCycles.remove(cycle)
            checkAngle = False
        elif not cycle[2]:
            if cycle[1] == (len(keyFrames)-1):
                allCycles.remove(cycle)
                checkAngle = False
            else:
                cycle[2] = len(keyFrames)-1
        
        #angle difference correction (Not touching the mess I made above)
        if checkAngle:
            angle1 = abs(anglesPerFrame[keyFrames[cycle[0]][1]][cycle[4]] - anglesPerFrame[keyFrames[cycle[1]][1]][cycle[4]])
            angle2 = abs(anglesPerFrame[keyFrames[cycle[1]][1]][cycle[4]] - anglesPerFrame[keyFrames[cycle[2]][1]][cycle[4]])

            if angle1 > angle2:
                cycle[3] = angle1
            else: 
                cycle[3] = angle2

    #print(f"allCycles: {allCycles}")


    #get reps without model           #Not using getCloser for now
    #if not workout:
    parallel = getTrend(allCycles, anglesFromExtracted, int(repNumber))
    # else:
    #     if repNumber:
    #         parallel = getCloser(allCycles, anglesFromExtracted, model, int(repNumber))
    #     else:
    #         parallel = getCloser(allCycles, anglesFromExtracted, model)

    #print(f"cycles: {parallel}")

    return parallel, modelName, importantAngles, excludeAngles


# TODO EXPLAIN THIS
def getTrend(cycles, allAngles, repNumber = 9999):
    #cycle [start, turning point, end, angle]

    reps = []


    for cycleJoint in cycles:
        
        if cycleJoint[3] < math.radians(5): #remove cycles under 5 degrees
            cycles.remove(cycleJoint)

    #print(f"all cycles before pairs: {cycles}\n")
    pairs = getPairs(cycles)
    pairList = []
    for pair in pairs:
        pairList.append(cycles[pair[0]])

    if len(pairList) == repNumber:
        return pairList 
        
    for cycle in cycles:
        if containsCycle(cycle, pairList):
            #print("removing cycle")
            cycles.remove(cycle)

    # print(f"pairlist: {pairList}\n")
    # print(f"pairlesslist: {cycles}\n")
    
    reps = pairList

    for i in range(len(cycles)):
        cycle = pickLargest(cycles)
        parallelAngle = getParallelCycleAngle(cycle, allAngles)
        cycles.remove(cycle)
        #print(f"Parallel angle: {parallelAngle}")
        if parallelAngle and parallelAngle > math.radians(5):
            #print("angle is big enough") 
            if (len(reps) < repNumber) and checkValidRange(cycle, reps):
                #print(f"inserting {cycle} in {reps}\n")
                reps = insertRep(reps, cycle)
            # elif len(reps) < repNumber:
            #     print(f"len(reps): {len(reps)} < repNumber: {repNumber} but not in range")
            # else:
            #     print(f"len(reps): {len(reps)} < repNumber: {repNumber} is false")
                
        # else:
        #     if parallelAngle:
        #         print(f"parallel angle too small: {parallelAngle}")
        #     else:
        #         print(f"no parallel angle gotten for {cycle}")
    
    return reps

def containsCycle(cycle, list):
    for i in list:
        if i[0] == cycle[0]\
            and i[1] == cycle[1]\
            and i[2] == cycle[2]:
            return True
    return False


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
    #print(f"\nChecking if {cycle} fits in {reps}")

    for rep in reps:
        if rep[0] <= cycle[0] and rep[2] > cycle[0]:
            #print("cycle starts in between reps")
            return False
        elif rep[0] < cycle[2] and rep[2] >= cycle[2]:
            #print("cycle ends in between reps")
            return False
    #print("It does")
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

    return getReps(extracted, allAngles, 9999, modelName)


# TODO ??????????
def makeNewModelV2():
    #print(f"Reps: {reps}")
    model = {}
    modelName, importantJoints, excludeJoints = setupNewWorkout()
    importantAngles = convertJoints(importantJoints)
    excludeAngles = convertJoints(excludeJoints)
    model["ImportantAngles"] = importantAngles
    model["ExcludeAngles"] = excludeAngles
    modelDir = str(os.path.dirname(__file__)) # to ComputerVisionTest
    modelName = modelName.replace(" ","_")
    models = str(modelDir) + "\\models\\"
    path = models + modelName + ".json"
    #this is to the directory outside the commit of git to get to videos for ml_traing
    vid_dir = str(Path(modelDir).resolve().parents[2]) + "\\ML_training\\"
    correct_dir =  vid_dir + f"\\correct_trainML\\{modelName}"
    incorrect_dir = vid_dir + f"\\incorrect_trainML\\{modelName}" 
    if os.path.exists(correct_dir) == False:
        os.mkdir(correct_dir)
    else:
        print("the directory for this workout exists")
    
    if os.path.exists(incorrect_dir) == False:
        os.mkdir(incorrect_dir)
    else:
        print("the directory for this workout exists")
    with open(path, 'w') as f:
        json.dump(model, f)

    return model


# Compute a dataframe from the provided videos and then save it
def computeData(modelName):
    vidsDir = Path.cwd().parents[0]
    # paths = [vidsDir + "\\vids\\good_trainML\\", # good reps folder
    #          vidsDir + "\\vids\\bad_trainML\\"] # bad reps folder
    paths = [str(vidsDir) + f"\\ML_training\\correct_trainML\\{modelName}\\", # good reps folder
             str(vidsDir) + f"\\ML_training\\incorrect_trainML\\{modelName}\\"] # bad reps folder
    #put threads or mulitprocessing here
    
    goodOrBad = 1 # lengths of good reps
    frames =[]
    for path in paths: #first good paths, then bad paths
        items = []
        allReps = []
        totalAngles = []
        for filename in os.listdir(path):
            args = (path, filename, modelName)
            items.append(args)
        print(f"items(path, filename, modelName): {len(items)}")
        numProcessors = mproc.cpu_count()-1 # one less than max so server has one open core
        with mproc.Pool(processes=numProcessors) as pool:
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
        
        df = mli.repsToDataframe(allReps, totalAngles, goodOrBad, excludeAngs)
        shaper = tf.shape(df)
        print(f"\nthis is df.shape before merge: {shaper}\n")
        #print(f"\nthis is df before merge: {df}\n")
        
        # prep for bad vids
        frames.append(df)
        goodOrBad = 0
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
def vid_ML_eval(modelName,trained_MLmodel, vid_path):

    extracted, allAngles, _ = getKeyFramesFromVideo(vid_path)
    keyAngs = []
    print(f"these are the all angles: {len(allAngles)}")
    #error is caused here due to all angles is not cut down by the frames.remove(frame)
    #keeping the allangles to be still the size of the video
    for frame in extracted:
        if frame[1] < len(allAngles):
            keyAngs.append(allAngles[frame[1]])
        else:
            del extracted[-1]
    
    reps, modelName, importantAngles, exclude_angles = getReps(extracted, allAngles, workout=modelName)
    df = mli.dataframeforeval(reps, keyAngs, exclude_angles)
    print(f"amount of reps: {reps}")
    rep_list, frame_rep_list, y_pred= mli.vid_ml_eval(modelName,trained_MLmodel, df, extracted, reps, importantAngles)
    print(f"rep_list: {rep_list}\n\n frame_rep_list: {frame_rep_list}")
    return rep_list, extracted, y_pred


# method to contain the entire video evaluation process, model loading, and 
# video output
def evaluate_video(name, path):
    # try:
            #this is to load model to get the important angles to display on vid
            modelDir = str(os.path.dirname(__file__))
            imp_path = f"{str(modelDir)}\\models\\"
            model = Workout().loadModel(f"{imp_path}{name}.json")
            importantAngles = model.getImportantAngles()
            #this is to load model for predict
            model_path = modelDir + "\\machineLearning\\ML_Trained_Models\\"+ str(name)+"_trained"
            load_model = tf.keras.models.load_model(model_path)
            acutal_frame_list, extracted, y_pred =vid_ML_eval(name,load_model, path)
            
            
            extracted_frame_list = [x[1] for x in extracted]
            #rep_frame_sets is using rep list to get the indexes of all frames needed
            rep_frame_sets = []
            #this for loop grab the 3 first iteams in actual frames which are the frame number
            #last number is the angle
            for rep_set in acutal_frame_list:
                rep_frame_sets.append(extracted_frame_list[rep_set[0]])
                rep_frame_sets.append(extracted_frame_list[rep_set[1]])
                rep_frame_sets.append(extracted_frame_list[rep_set[2]])
            
            final_frame_list = []
            #this than makes the list into a list of list
            #eg. [[up frame, down frame, up frame], [up frame,down frame,up frame]]
            for i in range(0,len(rep_frame_sets),3):
                if len(rep_frame_sets[i:i+3]) == 3:
                    final_frame_list.append(rep_frame_sets[i:i+3])
            #start of debugging
            if actual_rep_frame_display == True:
                print(f"rep_frame_sets: {rep_frame_sets}")
                print(f"final_frame_list: {final_frame_list}")
            
                cap = cv2.VideoCapture(path)
                max_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                print(f"max_frames: {max_frames}")
                constant_height = 700
                for i in rep_frame_sets:

                    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                    success, img = cap.read()
                    height = img.shape[0]
                    width = img.shape[1]
                    height_percentage = float(constant_height/int(height))
                    modded_width = int(float(width)*height_percentage)
                    cv2.putText(img, f"{str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))}, rep_frame_sets, frame #: {i}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                    resize = cv2.resize(img, (modded_width, constant_height))
                    cv2.imshow("Image", resize)
                    key = cv2.waitKey(0)  #millisecond delays
                    if key == 27: #esc
                        cv2.destroyWindow("Image")
                cap.release()
            #end of debuggin
            #using fianl frame which are the list of list of each rep we can 
            #than dpisplay each rep as its own video through another py file function
            prediction = []
            for pred_index in range(len(y_pred)):
                prediction.append(y_pred[pred_index][0])
                print(prediction)
            poseDisplay.capture_feed(path, final_frame_list, prediction, importantAngles, name)
            # except:
            #     print("\nModel name does not exist. create model using option 4")
            #     print("Models that exist are:")
            #     model_path = str(vidsDir) + "\\ML_Trained_Models\\"
            #     count = 1
            #     for filename in os.listdir(model_path):
            #         print(f"{count}: {filename}")
            #mli.vid_ml_eval(name, path)

#this function was made so that there are less errors in inputting 
#due to typing everytime has a higher chance of errors so
#this function gets all created models and puts them in a list
#to choose from using digits
def get_user_input(allow_create=False):
    model_path = str(os.path.dirname(__file__)) + "\\models\\"
    model_choices = []
    n = 1
    print("\nlist of trained models:")
    #this for loop prints the models name without the .json
    for model_name_json in os.listdir(model_path):
        model_name = os.path.splitext(model_name_json)
        print(f"{n}. {model_name[0]}")
        
        model_choices.append(model_name[0])
        n = n+1
    if allow_create:
        model_choices.append("Create new workout")
        n = n+1
    #this is to get user choice so that there are less errors
    user_choice = input("choose the number of the workout you want to check: ")
    error_amnt = 0
    while user_choice.isdigit() == False or int(user_choice) > len(model_choices) or int(user_choice)<= 0:
        error_amnt = error_amnt +1
        if error_amnt == 3:
            error_amnt = 0
            print("\nlist of trained models:")
            n= 1
            for model in model_choices:
                print(f"{n}. {model}")
                n = n+1
            
        print("invalid choice")
        user_choice = input("choose the number of the workout you want to check: ")
    user_choice = int(user_choice) - 1
    if user_choice < len(model_choices):
        name = model_choices[user_choice]
    else:
        name = input("Enter name of new workout: ")
    name = name.replace(" ","_")
    return name

if __name__ == "__main__":
    
    MENU2 = """
    Choices:
    1. Create New Rep Model
    2. Compute dataframe from videos
    3. Train,Test, and save Machine Learning Analysis 
    4. load existing Machine learning model for video input
    5. Quit\nChoice: """
    print(f"os.getcwd(): {os.getcwd()}")
    dir_name = str(os.path.dirname(__file__))
    print(dir_name)
    dir_up = Path(dir_name).resolve().parents[2]
    print(f"str(os.path.dirname(__file__)): {dir_up}")
    while True:
        choice = input(MENU2)
        if choice == "1":
            # video = input("Path to video: ").strip("'")
            # extracted, allAngles,impangs = getKeyFramesFromVideo(video)
            model = makeNewModelV2()
            print(f"New workout added\n")

        elif choice == "2":
            name = get_user_input(allow_create=True)
            print(f"Workout chosen: {name}")
            name = name.replace(" ","_")
            computeData(name)
            
        elif choice == "3":
            name = get_user_input(allow_create=True)
            print(f"Workout chosen: {name}")
            name = name.replace(" ","_")
            trained_model = open_and_train(name)

        elif choice == "4":
            name = get_user_input()
            print(f"Workout chosen: {name}")
            path = input("video to check: ")
            # cwd = str(os.path.dirname(__file__))
            evaluate_video(name, path)
            

        elif choice == "5" or choice == "q":
            break

        else:
            print("Incorrect input, try again.")
            continue

        