#posemodule plus binary classifier most current one

import time
import math
import cv2
import mediapipe as mp
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mathutility
from binomialFitting import PoseUtilities
import os
from pathlib import Path

#this is just for transferring angle id back to blaze pose
angle_point = [0,0,11,11,11,11,23,23,12,12,24,24,13,25,14,26]
#this is just the class to find and create the pose
# MODE:
#     mode set to false is for a video due to it will try to localize the landmarks to each other
#     mode set to True is for images due to 2 images can be completely different therefore does
#     not need to localize landmarks to be closer together
# SMOOTH: 
#     if set to True reduces jittering making it more smooth transition from each frame
#     if set to False does not try to reduce jittering in video
#     if mode is set to True for images it will be automatically ignored
# SEGMEN:
#     if True generates the segmentation mask for the pose
#     if False does not generate the segmentation mask
# SMOOTHSEG:
#     if set True will try to reduce the masks jitter on the images
#     if set False will not try to reduce the jitter
class poseDetector():

    def __init__(self, mode=False,modcomp = 2, smooth=True,segmen=True, smoothseg=True,
                 detectionCon=0.7, trackCon=0.5):

        self.mode = mode
        self.modcomp = modcomp
        self.smooth = smooth
        self.segmen = segmen
        self.smoothseg = smoothseg
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.low_angle = 360
        self.lowhip_angle = 360

        self.mpDraw = mp.solutions.drawing_utils #this is for drawing everything
        self.mpPose = mp.solutions.pose # this is for a model
        self.pose = self.mpPose.Pose(self.mode, self.modcomp, self.smooth, self.segmen, self.smoothseg,  self.detectionCon, self.trackCon) #this is for determining pose of person

    #this function tries to find a pose and draws it out
    #a pose is just the human body using lines and dots
    #dots are landmarks
    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #attempting to draw segmentation on image.
        annotated_img = img.copy()
        
        #print(results.pose_landmarks) print all landmarks aka points every frame

        if self.results.pose_landmarks:
            if draw:
                #landmarks are for the dots on the body there are 32 dots and self.mpPose.POSE_CONNECTIONS connects the dots
                self.mpDraw.draw_landmarks(annotated_img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS) 
                #self.mpDraw.plot_landmarks(self.results.pose_world_landmarks,self.mpPose.POSE_CONNECTIONS)
        return annotated_img

    #this will be used to get each position of each landmark and label them
    def findPosition(self,img, draw=True):
        self.lmList =[] #landmark list
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape # we need this because
                #print(id, lm)
                cx, cy, cc, cv = int(lm.x * w), int(lm.y * h), float(lm.z), float(lm.visibility) #this gives the pixel point of the landmarks
                self.lmList.append([id,cx,cy,cc,cv])
                #if found checks if can draw it if can draw
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)#this will over lay on points if seeing properly it would be blue
                    cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        return self.lmList
    
    def seg_mask(self,img,draw = True):
        # this is the condition on making it either grey or not
        annotated_img = img.copy()
        condition = np.stack((self.results.segmentation_mask,), axis =-1)> 0.1
        bg_img = np.zeros(img.shape, dtype = np.uint8)
        bg_img[:] = (192,192,192)
        annotated_img = np.where(condition,annotated_img, bg_img)
        return annotated_img
    
    def threeDimensionalplot(self,img):
        ax = plt.axes(projection = "3d")
        ax.scatter(3,5,7)
        plt.pause(0.1)
        return plt
    
    #this is using the segmentation mask variable of confidence to measure out where the beginning
    #of the back is from the side view
    def backLine(self,img,x1,y1,x2,y2,perp_slope,y1_intercept,y2_intercept):
        height =img.shape[0]
        width = img.shape[1]
        if self.results.pose_landmarks:
            confidence = self.results.segmentation_mask[y1][x1]
            #print(confidence)
            plt1 = x1,y1
            plt2 = x2,y2
            cur_x = x1
            cur_y = y1
            while confidence > 0.1 and cur_x <width and cur_y < height:
                cur_x = cur_x -1
                cur_y = int(perp_slope*cur_x+y1_intercept)
                if cur_y< height:
                    confidence=self.results.segmentation_mask[cur_y][cur_x]
            plt1 = cur_x,cur_y
            confidence = self.results.segmentation_mask[y2][x2]
            cur_x2 = x2
            cur_y = y2
            while confidence > 0.1 and cur_x2 < width and cur_y < height:
                cur_x2 = cur_x2 -1
                cur_y = int(perp_slope*cur_x2+y2_intercept)
                if(cur_y< height):
                    confidence=self.results.segmentation_mask[cur_y][cur_x2]
            plt2 = cur_x2,cur_y
        return cur_x, cur_x2
    
    def findWorldPosition(self,img, draw=False):
        mod_lmList =[] #modded landmark list for actual pixels
        self.world_lmList = [] #modded landmark list for real world estimitation
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_world_landmarks.landmark):
                h, w, c = img.shape # we need this to be able to get exact location 
                #of point as a pixel on the screen
                #print(id, lm)
                cx, cy, cz, cv = int(lm.x * w), int(lm.y * h), int(lm.z), float(lm.visibility) #this gives the pixel point of the landmarks
                mod_lmList.append([id,cx,cy,cz,cv])
                self.world_lmList .append([id,lm.x,lm.y,lm.z])
                #if found checks if can draw it if can draw
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)#this will over lay on points if seeing properly it would be blue
                    #cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        return mod_lmList, self.world_lmList , self.results.pose_world_landmarks
    
    # fix the line on the back for every thing
    # this may be used by checking which way the face is facing to create the line
    #crashes cuz can't find back beginning it is out of screen
    def checkback(self,img,backplt1,backplt2):
        x1, y1 = backplt1
        x2, y2 = backplt2
        if x2-x1 != 0:
            slope= (y2-y1)/(x2-x1)
            y_int = (y1-(slope*x1))
            for i in range(min(x1,x2),max(x1,x2)-2):
                cur_y = int(slope*i + y_int)
                try:
                    confidence = self.results.segmentation_mask[cur_y][i]
                except:
                    return True
                if(confidence > 0.1):
                    return False
        return True
    
    def face_track(self,img,lmList):
        height = img.shape[0]
        for i in range(len(lmList)):
            if lmList[i][0] == 0:
                noseX = lmList[i][1]
                noseY = lmList[i][2]
            elif lmList[i][0] == 8:
                earX = lmList[i][1]
                earY = lmList[i][2]
        cur_x = earX
        cur_y = earY
        slope = 0
        if noseX -earX != 0:
            slope = (noseY - earY)/(noseX - earX)
           # print(f"face slope: {slope}")
            y_int = int(cur_y - (slope*cur_x))
            if cur_y > height:
                cur_y = height
            confidence = self.results.segmentation_mask[cur_y][cur_x]
            while confidence >0.1:
                cur_x = cur_x - 1
                cur_y = int((slope*cur_x) + y_int)
                if cur_y < height:
                    confidence = self.results.segmentation_mask[cur_y][cur_x]
            cur_x = cur_x - 5
            cur_y = int((slope*cur_x) + y_int)
            if cur_y < height:
                confidence = self.results.segmentation_mask[cur_y][cur_x]
        return cur_x, cur_y, noseX, noseY, int(slope)
    
    def findkneeAngle(self,img,p1,p2,p3, draw=True):
        x1,y1 = self.lmList[p1][1:3]
        x2,y2 = self.lmList[p2][1:3]
        x3,y3 = self.lmList[p3][1:3]
        point1 = np.array(self.lmList[p1][1:4])
        point2 = np.array(self.lmList[p2][1:4])
        point3 = np.array(self.lmList[p3][1:4])
        #this is to calaculate the angle if you have 3 points
        angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2))
        if angle >= 0:
            angle = 360-angle
        else:
            angle = abs(angle)
        #print(angle)
        if angle< self.low_angle:
            self.low_angle = angle
        if draw:
            cv2.circle(img,(x1, y1), 10, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x1, y1), 15, (0,0,255),2)
            cv2.circle(img,(x2, y2), 5, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x2, y2), 15, (0,0,255),2)
            cv2.circle(img,(x3, y3), 5, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x3, y3), 15, (0,0,255),2)
            cv2.putText(img, str((int(angle))),(x2-20,y2+50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
        return self.low_angle
    
    def findhipAngle(self,img,p1,p2,p3, draw=True):
        x1,y1 = self.lmList[p1][1:3]
        x2,y2 = self.lmList[p2][1:3]
        x3,y3 = self.lmList[p3][1:3]
        point1 = np.array(self.lmList[p1][1:4])
        point2 = np.array(self.lmList[p2][1:4])
        point3 = np.array(self.lmList[p3][1:4])
        #this is to calaculate the angle if you have 3 points
        angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2))
        #print(angle)
        if angle< self.lowhip_angle:
            self.lowhip_angle = angle
        if draw:
            cv2.circle(img,(x1, y1), 10, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x1, y1), 15, (0,0,255),2)
            cv2.circle(img,(x2, y2), 5, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x2, y2), 15, (0,0,255),2)
            cv2.circle(img,(x3, y3), 5, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x3, y3), 15, (0,0,255),2)
            cv2.putText(img, str(int(angle)),(x2-20,y2+50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
        return self.lowhip_angle

    def set_angle(self,img,importantAngles, angle_landmark, draw=True):
        index = 0
        for imp_angle in importantAngles:
            x1,y1 = self.lmList[imp_angle][1:3]
            radian_angle = angle_landmark[index]
            degrees = math.degrees(radian_angle)
            index = index+1
            if draw:
                cv2.circle(img,(x1, y1), 10, (0,0,255),cv2.FILLED)
                cv2.circle(img,(x1, y1), 15, (0,0,255),2)
                cv2.putText(img, str(int(degrees)),(x1-20,y1+50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)

##
# This function is to get the videos and send it to the class pose detector to than
# add in the landmarks and connect them it also gets the angles, and landmark list
# This also detects the curvature of the back
# Parameters: video path
# returns: lowest angle
##           
def capture_feed(path, frame_rep_list, prediction, importantAngles, model_name):
    print(f"important angles: {importantAngles}")
    print(f"this is path: {path}")
    cap = cv2.VideoCapture(path)  # the video sys.path[0] is the current path of the file
    pTime = 0
    detector = poseDetector()
    #data = np.empty((3,32,length))
    frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    success = True
    print(f"frame_rep_list: {frame_rep_list}, length: {len(frame_rep_list)}")# length is the amount of reps in video
    constant_height = 700
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    height_percentage = float(constant_height/int(frame_height))
    modded_width = int(float(frame_width)*height_percentage)
    save_size = (modded_width,constant_height)
    #this is to set up all directories for the the eval to save the workouts
    dir_name = str(os.path.dirname(__file__))
    dir_up = str(Path(dir_name).resolve().parents[2])
    userpath = dir_up+"/Users"
    if os.path.exists(userpath) == False:
        os.mkdir(userpath)
    username = input("please input user name: ")
    username_dir = userpath+f"/{username}"
    if os.path.exists(username_dir) == False:
        os.mkdir(username_dir)
    username_dir_workout = username_dir+ f"/{model_name}"
    if os.path.exists(username_dir_workout) == False:
        os.mkdir(username_dir_workout)
    username_dir_workout_bad = username_dir+ f"/{model_name}/Bad_reps"
    if os.path.exists(username_dir_workout_bad) == False:
        os.mkdir(username_dir_workout_bad)
        
    username_dir_workout_good = username_dir+ f"/{model_name}/Good_reps"
    if os.path.exists(username_dir_workout_good) == False:
        os.mkdir(username_dir_workout_good)
    
    #this iterates through each rep to show the video of that individual rep
    for rep in range(len(frame_rep_list)):
        if prediction[rep] < 0.75:
            result = cv2.VideoWriter(f'{username_dir_workout_bad}/{model_name}{rep}.mp4',cv2.VideoWriter_fourcc(*'mp4v'),10,save_size)
        else:
            result = cv2.VideoWriter(f'{username_dir_workout_good}/{model_name}{rep}.mp4',cv2.VideoWriter_fourcc(*'mp4v'),10,save_size)
        start_frame_id = frame_rep_list[rep][0]# start up
        end_frame_id = frame_rep_list[rep][2]# end up
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_id) # setting video to the up position
        while success:
            #this sees if it can read the frame that it is given
            success, img = cap.read()
            
            slope = 0
            perp_slope = 0
            if success == False:
                break
            
            if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) == end_frame_id:
                #cv2.destroyWindow("Image")
                break
            
            # img.shape is a list of the dimensions of the frame 0 = height
            # 1 = width, 2 = number of chnnels for image
            height = img.shape[0]
            width = img.shape[1]
            
            
            img = detector.findPose(img)
            #this is the annotated image with the segmentation mask it is needed as a copy
            #of the first image so that they are 2 seperate images so that all the colours will not
            #be the same
            annotated_img = detector.seg_mask(img)
            lmList = detector.findPosition(annotated_img)
            world_mod_lmList, world_unmod_lmlist, world_landmarks = detector.findWorldPosition(annotated_img)
            #print(world_unmod_lmlist[12][1], world_unmod_lmlist[12][2], world_unmod_lmlist[12][3])
            #print(world_unmod_lmlist[24][1], world_unmod_lmlist[24][2], world_unmod_lmlist[12][3])
            mathutility.HighVis(lmList)
            for i in range(len(lmList)):
                #shoulder right
                if lmList[i][0] == 12:
                    x1 = int(lmList[i][1])
                    y1 = int(lmList[i][2])
                    pt1 = (x1,y1)
                    
                #hip right
                elif lmList[i][0] == 24:
                    x2 = int(lmList[i][1])
                    y2 = int(lmList[i][2])
                    pt2 = (x2 ,y2)
                elif lmList[i][0] == 8:
                    earX = lmList[i][1]
                    earY = lmList[i][2]
            cv2.line(img,pt1,pt2,(139,0,0),2)
            
            #this is due to if the line is completely verical
            if x2-x1 != 0:
                slope = ((y2-y1)/(x2-x1))
                
            y_inter = (y1-(slope*x1)) 
            #print(f"slope: {slope}, y_inter: {y_inter}, x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")
            
            
            #also for case for completely vertical 
            perp_y_inter = 0 
            #this is for when the slope tries to flip to a negative number causing the perp lines to be on the chest
            if slope != 0:
                if slope > 0:
                    perp_slope = (-1)/slope
                    cv2.putText(annotated_img, f"perp slope(-1/slope >0): {perp_slope}", (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                else:
                    perp_slope = (-1)/slope
                    cv2.putText(annotated_img, f"perp slope(-1/slope): {perp_slope}", (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            
            perp_y_inter = int(y1-(perp_slope*x1)) 
            #shoulder
            cv2.line(annotated_img,pt1,(0,perp_y_inter),(0,128,0),6)
            perp_y_inter_bottom = int(y2-(perp_slope*x2))
            #hip out
            cv2.line(annotated_img,pt2,(0,perp_y_inter_bottom),(0,128,0),6)
            if y2 >img.shape[0]:
                y2 = img.shape[0]-1
            
            backx, backx2 = detector.backLine(img,x1,y1,x2,y2,perp_slope,perp_y_inter,perp_y_inter_bottom)
            #print(f"back point1: {backx}, back point2: {backx2}")
            backplt1 = backx-10, int(perp_slope*(backx-10)+perp_y_inter)
            backplt2 = backx2-10, int(perp_slope*(backx2-10)+perp_y_inter_bottom)


            arch= detector.checkback(img,backplt1,backplt2)
            #this is for the upper back to lower back checking back posture
            if arch == True:
                cv2.line(annotated_img,backplt1,backplt2,(0,128,0),6)
            else:
                cv2.line(annotated_img,backplt1,backplt2,(0,0,128),6)


            #prints list of landmarks from 1 to 32 look at mediapipe diagram to know what landmark is which bodypart
            #print(lmList)
            
            cTime = time.time()
            #print(f"real world measurements: {world_unmod_lmlist}")
            fps = 1 / (cTime - pTime)
            pTime = cTime
            #returns angles of frame goes head lr, head bf, body lr, head bf, lshoulder Fb, lshoulder ud,
            #Lhip lr, Lhip Fb, rshoulder Fb, rshoulder ud, rhip lr, rhip Fb, lelb, lknee, relb, rknee
            cur_all_angs = PoseUtilities.compute_body_angles(world_landmarks)
            #print(f"curall: {cur_all_angs}")
            #this uses our vector mapping to get 3d angles and plant it on the video
            if len(lmList) != 0:
                angle_at_landmark = []
                actual_landmark = []
                for angle_place in importantAngles:
                    angle_at_landmark.append(cur_all_angs[angle_place])
                    actual_landmark.append(angle_point[angle_place])
                detector.set_angle(annotated_img,actual_landmark,angle_at_landmark)
            #this uses the 2d image to get the angles
            # if len(lmList) != 0:
            #     angle = detector.findkneeAngle(annotated_img,24,26,28) #delete
            #     angle2 = detector.findkneeAngle(annotated_img,23, 25, 27) #delete
            #     hip_angle = detector.findhipAngle(annotated_img,12, 24, 26) #delete
                #print(f"lowest angle; {angle}")
            cv2.putText(annotated_img, f"{str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))}, {end_frame_id}, rep #: {rep}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            #resize is width than height
            resize = cv2.resize(annotated_img, (modded_width, constant_height))
            #print(f"this is angle from blaze pose {angle2} vs {new_angle}. parallel knee: {angle} ")
            result.write(resize)
            key = cv2.waitKey(1)  #millisecond delays
            if key == 27: #esc
                cv2.destroyWindow("Image")
                break
    result.release()
    cap.release()
    # print(f"list of bad rep dir: {username_dir_workout_bad}")
    # for bad_rep_vid in os.listdir(username_dir_workout_bad):
    #     print(f"this is bad rep vid: {bad_rep_vid}")
    #     cap2 = cv2.VideoCapture(os.path.join(username_dir_workout_bad, bad_rep_vid))
    #     print(os.path.join(username_dir_workout_bad, bad_rep_vid))
    #     success = True
    #     while success:
    #         success, img2 = cap2.read()
    #         if img2 == None:
    #             height = 0
    #             width = 0
                
    #         else:
    #             height = img2.shape[0]
    #             width = img2.shape[1]
    #         # if success == False:
    #         #     print("Could not open video")
    #         #     break
    #         if height >0 & width>0:
    #             cv2.imshow("Frame", img2)
    #     cv2.destroyAllWindows
    #     cap2.release()
    #return int(angle), int(angle2), int(hip_angle)