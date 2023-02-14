#posemodule plus binary classifier most current one

import time
import math
import cv2
import mediapipe as mp
import sys
import numpy as np
import matplotlib.pyplot as plt
import vg
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mathutil

# all in inches
# these are all length to each body part from blaze pose

#JEan carlos Gonzales Graces
JCface = [2,1.5,4,2,1.5,4,2,]#nose-L inner eye, L inner eye - L outer eye, L outer eye - L ear, 
#nose - R inner eye, R inner eye - R outer eye, R outer eye - R ear
JCarm = [12.5, 10] #shoulder - elbow, elbow to wrist 
JCtorso = [14.25, 21.5, 14] # shoulder - shoulder, shoulder to hip, hip to hip
JCleg = [14.63, 15.25] # hip to knee, knee to ankle

#Orifzon Hawz
Orfiface = [2, 1.88, 4, 2, 1.88, 4] #nose-L inner eye, L inner eye - L outer eye, 
#L outer eye - L ear, nose - R inner eye, R inner eye - R outer eye, R outer eye - R ear
Orfiarm = [11.5, 11.38] #shoulder to elbow, elbow to wrist
Orfitorso = [15,22, 14] # shoulder to shoulder, shoulder to hip, hip to hip
Orfileg = [16,17.88] # hip to knee, knee to ankle


#this is just the class to find and create the pose
class poseDetector():

    def __init__(self, mode=False,modcomp = 2, smooth=True,segmen=True, smoothseg=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.modcomp = modcomp
        self.smooth = smooth
        self.segmen = segmen
        self.smoothseg = smoothseg
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.low_angle = 360

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
    
    def findWorldPosition(self,img, draw=True):
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
        return mod_lmList, self.world_lmList 
    
    def checkback(self,img,backplt1,backplt2):
        x1, y1 = backplt1
        x2, y2 = backplt2
        if x2-x1 != 0:
            slope= (y2-y1)/(x2-x1)
            y_int = (y1-(slope*x1))
            for i in range(min(x1,x2),max(x1,x2)-2):
                cur_y = int(slope*i + y_int)
                confidence = self.results.segmentation_mask[cur_y][i]
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
    
    ##
    # find world angle does not work right now but
    # This grabs the landmarks in a 3d space and creates them
    # origin is the mid waist
    # parameters: the class itself 
    ##
    def findWorldAngle(self,img,p1,p2,p3, draw=True):
        x1,y1 = self.lmList[p1][1:3]
        x2,y2 = self.lmList[p2][1:3]
        x3,y3 = self.lmList[p3][1:3]
        point1 = np.array(self.lmList[p1][1:4])
        point2 = np.array(self.lmList[p2][1:4])
        point3 = np.array(self.lmList[p3][1:4])
        #this is to calaculate the angle if you have 3 points
        angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2))
        print(360 -angle)
        if draw:
            cv2.circle(img,(x1, y1), 10, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x1, y1), 15, (0,0,255),2)
            cv2.circle(img,(x2, y2), 5, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x2, y2), 15, (0,0,255),2)
            cv2.circle(img,(x3, y3), 5, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x3, y3), 15, (0,0,255),2)
            cv2.putText(img, str((int(360-angle))),(x2-20,y2+50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
    
    # to get vector a**2 + b**2 + c**2 = d**2
    def digitalToReal(self, body, leg):
        lmList = self.lmList
        chest = body[0]
        torso = body[1]
        waist = body[2]
        thigh = leg[0]
        shin = leg[1]
        rshoulderx = lmList[12][1]
        rshouldery = lmList[12][2]
        rhipx = lmList[24][1]
        rhipy = lmList[24][2]
        lengthy = abs(rhipy - rshouldery)
        lengthx = abs(rhipx - rshoulderx)
        length = math.sqrt(lengthy**2 + lengthx**2)
        
        lhipx = lmList[23][1]
        lhipy = lmList[23][2]
        
        rkneex = lmList[26][1]
        rkneey = lmList[26][2]
        
        lkneex = lmList[25][1]
        lkneey = lmList[25][2]
        
        lanklex = lmList[27][1]
        lankley = lmList[27][2]
        
        print(f"this is the length {length}")
        if( len(lmList)>= 32):
            ratio = torso/length
            print(f"this is the ratio {ratio}feet/pixel")
            thighlen = math.sqrt(abs(rkneex - rhipx)**2 + abs(rkneey - rhipy)**2)*ratio
            print(f"thigh orfi = 16 while {thighlen}") #thigh len increases because knee goes out causing increase in size
            pixel_len = waist/ratio # what it is supose to be
            
            #this is to get depth of the z axis through math
            lenhipx = (lhipx - rhipx)**2
            lenhipy = (lhipy - rhipy)**2
            lenpixel = pixel_len**2
            hipzlen = math.sqrt(lenpixel -lenhipx  - lenhipy)
            print(f"hip z (14) {hipzlen*ratio}")
            
            #this is to get the other knee
            lenthighx = (lkneex - lhipx)**2
            lenthighy = (lkneey - lhipy)**2
            lenthighpixel = (thigh/ratio)**2
            print(f"{lenthighpixel}-{lenthighx}-{lenthighy} = {lenthighpixel - lenthighx - lenthighy}")
            if lenthighpixel - lenthighx - lenthighy >= 0:
                lkneez = hipzlen + math.sqrt(lenthighpixel - lenthighx - lenthighy)
                print(f"knee z {lkneez*ratio}")
            else:
                lkneez = hipzlen
                print(f"knee z {lkneez*ratio}")
            
            lenanklex = (lanklex - lkneex)**2
            lenankley = (lankley - lkneey)**2
            lenanklepixel = (shin/ratio)**2
            if lenanklepixel - lenanklex - lenankley >= 0:
                lanklez = lkneez + math.sqrt(lenanklepixel - lenanklex - lenankley)
                print(f"ankle z {lanklez*ratio}")
            else:
                lanklez = lkneez
                print(f"ankle z {lanklez*ratio}")
            vecA = (lhipx -lkneex, lhipy - lkneey, hipzlen - lkneez)
            vecB = (lanklex - lkneex, lankley - lkneey, lanklez - lkneez)
            prod, angle  = angle_dot(vecA, vecB)
            print( prod, angle)
            return angle

def angle_dot(a, b):
    dot_product = np.dot(a, b)
    prod_of_norms = np.linalg.norm(a) * np.linalg.norm(b)
    angle = round(np.degrees(np.arccos(dot_product / prod_of_norms)), 1)
    return round(dot_product, 1), angle
            


##
# This function is to get the videos and send it to the class pose detector to than
# add in the landmarks and connect them it also gets the angles, and landmark list
# This also detects the curvature of the back
# Parameters: video path
# returns: lowest angle
##           
def capture_feed(vidname, torso, leg):
    cap = cv2.VideoCapture(sys.path[0]+ vidname)  # the video sys.path[0] is the current path of the file
    pTime = 0
    detector = poseDetector()
    #data = np.empty((3,32,length))
    frame_num = 0
    success = True
    new_angle = 360
    
    while success:
        #this sees if it can read the frame that it is given
        success, img = cap.read()
        constant_height = 700
        slope = 0
        perp_slope = 0
        if success == False:
            break
        # img.shape is a list of the dimensions of the frame 0 = height
        # 1 = width, 2 = number of chnnels for image
        height = img.shape[0]
        width = img.shape[1]
        height_percentage = float(constant_height/int(height))
        modded_width = int(float(width)*height_percentage)
        img = detector.findPose(img)
        #this is the annotated image with the segmentation mask it is needed as a copy
        #of the first image so that they are 2 seperate images so that all the colours will not
        #be the same
        annotated_img = detector.seg_mask(img)
        lmList = detector.findPosition(annotated_img)
        world_mod_lmList, world_unmod_lmlist = detector.findWorldPosition(annotated_img)
        print(world_unmod_lmlist[12][1], world_unmod_lmlist[12][2], world_unmod_lmlist[12][3])
        print(world_unmod_lmlist[24][1], world_unmod_lmlist[24][2], world_unmod_lmlist[12][3])
        mathutil.HighVis(lmList)
        for i in range(len(lmList)):
            if lmList[i][0] == 12:
                x1 = int(lmList[i][1])
                y1 = int(lmList[i][2])
                visibilty = int(lmList[i][4])
                pt1 = (x1,y1)
            elif lmList[i][0] == 24:
                x2 = int(lmList[i][1])
                y2 = int(lmList[i][2])
                visibilty2 = int(lmList[i][4])
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
        if slope != 0:
            perp_slope = (-1)/slope
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
        #the landmarks i want for side are 12 and 24 to get line and slope
        #plotting= detector.threeDimensionalplot(img)
        #print(world_lmList)

        #this gets the points to draw the line to the back of the head
        head_x, head_y ,noseX, noseY, head_slope= detector.face_track(img,lmList)
        arch2= detector.checkback(img,(head_x,head_y),backplt2)
        
        #this is to create the line from nose to back of head
        cv2.line(annotated_img,(noseX,noseY),(head_x,head_y),(0,128,0),6)

        #this is for from the back of head to hip checking for posture
        if arch2 == True:
            cv2.line(annotated_img,(head_x,head_y),backplt2,(0,128,0),6)
        else:
            cv2.line(annotated_img,(head_x,head_y),backplt2,(0,0,255),6)
        cTime = time.time()
        #print(f"real world measurements: {world_unmod_lmlist}")
        fps = 1 / (cTime - pTime)
        pTime = cTime
        if len(lmList) != 0:
            angle = detector.findkneeAngle(annotated_img,24,26,28)
            angle2 = detector.findkneeAngle(annotated_img,23, 25, 27)
            print(f"lowest angle; {angle}")
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        farkneeangle = detector.digitalToReal(torso, leg)
        if farkneeangle < new_angle:
            new_angle = farkneeangle
        #resize is width than height
        resize = cv2.resize(annotated_img, (modded_width, constant_height))
        cv2.imshow("Image", resize)
        key = cv2.waitKey(1)  # millisecond delays
        if key == 27: #esc
            cv2.destroyAllWindows
            break
    return int(angle), int(farkneeangle)

def binaryclassifier(degrees, labels, checks):
    # Step 2: Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(degrees, labels, test_size=0.2, random_state=0)

    # Step 3: Choose an appropriate machine learning model
    model = LogisticRegression()
    relen = len(degrees)
    reinnerlen = len(degrees[1])
    # Step 4: Train the model
    #breaks here
    model.fit(X_train, y_train)

    # Step 5: Evaluate the model
    #reshape is to make it understand the array for input into the logistic regression
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("Accuracy: ", accuracy) #accuracy = how often the model predicted correctly
    #this is determined by #of correct predictions # of total predictions
    
    print("Precision: ", precision) #prescion = how often the model predicted the event to be positive and it turned out to be true
    #this is determined by # of true positives/ (# of true positives + # of false positives)
    
    print("Recall: ", recall) #measures how good the model is at correctly predicting positive classes
    #this is determined by # of true positives/(# of true positives + # of false negatives)
    
    print("F1-Score: ", f1)# is the harmonic mean of precision and recall
    # harmonic mean is an alternative metric for the more common arithmetic mean. It is often useful when computing an average rate.
    # F1 score = 2 * ((precision * recall)/ (precision + recall))
    
    #the F1 score gives equal weight to Precision and Recall
    #   A model will obtain a high F1 score if both Precision and Recall are high
    #   A model will obtain a low F1 score if both Precision and Recall are low
    #   A model will obtain a medium F1 score if one of Precision and Recall is low and the other is high

    # Step 6: Make predictions
    #testign data below
    #new_data = np.array([80, 88, 89, 91, 92, 95])
    predictions = model.predict(checks)
    print(predictions)
    
    
def main():
    #these videos are for training of the binary classifier
    sen = mathutil.hello()
    print(sen)
    correctangleR1, correctangleL1 = capture_feed('/motioncapture/Correct_squat/SquatV1side.mp4', JCtorso, JCleg) #JC
    correctangleR2, correctangleL2 = capture_feed('/motioncapture/Correct_squat/SquatV2side.mp4', JCtorso, JCleg) #JC
    correctangleR3, correctangleL3 = capture_feed('/motioncapture/Correct_squat/SquatYV1side.mp4', JCtorso, JCleg) #random man
    correctangleR4, correctangleL4 = capture_feed('/motioncapture/Correct_squat/squatorfiside.mp4', Orfitorso, Orfileg) #orfi
    incorrectangleR1,incorrectangleL1 = capture_feed('/motioncapture/Incorrect_Squat/highsquatincorrectsideV1.mp4', JCtorso, JCleg) #Huu
    incorrectangleR2,incorrectangleL2 = capture_feed('/motioncapture/Incorrect_Squat/deepsquatincorrectV1.mp4', JCtorso, JCleg) #Huu
    incorrectangleR3,incorrectangleL3 = capture_feed('/motioncapture/Incorrect_Squat/highsquatorfiside.mp4',Orfitorso, Orfileg) #orfi
    incorrectangleR4,incorrectangleL4 = capture_feed('/motioncapture/Incorrect_Squat/deepsquatJCside.mp4', JCtorso, JCleg) #JC
    
    # Step 1: Collect and preprocess your data
    degrees = np.array([[correctangleR1, correctangleL1],[correctangleR2, correctangleL2],[correctangleR3, correctangleL3],
                        [correctangleR4, correctangleL4],[incorrectangleR1,incorrectangleL1], [incorrectangleR2,incorrectangleL2],
                        [incorrectangleR3,incorrectangleL3],[incorrectangleR4,incorrectangleL4]])
    #known labels of correctness
    labels = np.array([1,1,1,1,0,0,0,0])
    checkerangleR1, checkerangleL1  = capture_feed('/motioncapture/Incorrect_Squat/deepsquatJCside.mp4', JCtorso, JCleg) # 0
    checkerangleR2, checkerangleL2 = capture_feed('/motioncapture/Incorrect_Squat/highsquatorfiside.mp4', Orfitorso, Orfileg) # 0
    checkerangleR3, checkerangleL3 = capture_feed('/motioncapture/Correct_squat/SquatV2sideland.mp4', JCtorso, JCleg) # 1
    checkerangleR4, checkerangleL4 = capture_feed('/motioncapture/Incorrect_Squat/deepsquatorfiside.mp4', Orfitorso, Orfileg) # 0
    checkerangleR5, checkerangleL5 = capture_feed('/motioncapture/misc/Squatlarge1flipped.mp4', Orfitorso, Orfileg) # 0 false negative
    checks = np.array([[checkerangleR1, checkerangleL1],[checkerangleR2, checkerangleL2], [checkerangleR3, checkerangleL3],[checkerangleR4, checkerangleL4],[checkerangleR5, checkerangleL5]])
    binaryclassifier(degrees, labels, checks)
    return

if __name__ == "__main__":
    main()