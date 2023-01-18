import time

import cv2
import mediapipe as mp
import sys
import numpy as np
import matplotlib.pyplot as plt
#this is just the class to find and create the pose
class poseDetector():

    def __init__(self, mode=False,modcomp = 2, smooth=True,segmen=True, smoothseg=True,
                 detectionCon=0.7, trackCon=0.7):

        self.mode = mode
        self.modcomp = modcomp
        self.smooth = smooth
        self.segmen = segmen
        self.smoothseg = smoothseg
        self.detectionCon = detectionCon
        self.trackCon = trackCon

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
        lmList =[] #landmark list
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape # we need this because
                #print(id, lm)
                cx, cy, cc, cv = int(lm.x * w), int(lm.y * h), float(lm.z), float(lm.visibility) #this gives the pixel point of the landmarks
                lmList.append([id,cx,cy,cc,cv])
                #if found checks if can draw it if can draw
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)#this will over lay on points if seeing properly it would be blue
                    cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        return lmList
    
    def seg_mask(self,img,draw = True):
        # this is the condition on making it either grey or not
        annotated_img = img.copy()
        condition = np.stack((self.results.segmentation_mask,), axis =-1)> 0.1
        bg_img = np.zeros(img.shape, dtype = np.uint8)
        bg_img[:] = (192,192,192)
        annotated_img = np.where(condition,annotated_img, bg_img)
        return annotated_img
    
    def threeDimendionalplot(self,img):
        ax = plt.axes(projection = "3d")
        ax.scatter(3,5,7)
        plt.pause(0.001)
        return plt
    
    #this is using the segmentation mask variable of confidence to measure out where the beginning
    #of the back is from the side view
    def backLine(self,img,x1,y1,x2,y2,perp_slope,y1_intercept,y2_intercept):
        height =img.shape[0]
        width = img.shape[1]
        if self.results.pose_landmarks:
            confidence = self.results.segmentation_mask[y1][x1]
            print(confidence)
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
        lmList =[] #landmark list
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_world_landmarks.landmark):
                h, w, c = img.shape # we need this to be able to get exact location 
                #of point as a pixel on the screen
                #print(id, lm)
                cx, cy, cc, cv = int(lm.x * w), int(lm.y * h), int(lm.z), float(lm.visibility) #this gives the pixel point of the landmarks
                lmList.append([id,cx,cy,cc,cv])
                #if found checks if can draw it if can draw
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)#this will over lay on points if seeing properly it would be blue
                    #cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        return lmList
    
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
            print(f"face slope: {slope}")
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

def main():
    #comment only one line out videocapture of 0 is webcam videocapture than file is for vid
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(sys.path[0]+'/motioncapture/SquatV1side.mp4')  # the video sys.path[0] is the current path of the file
    pTime = 0
    detector = poseDetector()
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #data = np.empty((3,32,length))
    frame_num = 0
    success = True
    
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
        lmList = detector.findPosition(img)
        world_lmList = detector.findWorldPosition(img)
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
        print(f"slope: {slope}, y_inter: {y_inter}, x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")
        #this is the annotated image with the segmentation mask it is needed as a copy
        #of the first image so that they are 2 seperate images so that all the colours will not
        #be the same
        annotated_img = detector.seg_mask(img)
        
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
        print(f"back point1: {backx}, back point2: {backx2}")
        backplt1 = backx-10, int(perp_slope*(backx-10)+perp_y_inter)
        backplt2 = backx2-10, int(perp_slope*(backx2-10)+perp_y_inter_bottom)
        # arch= detector.checkback(img,backplt1,backplt2)
        # print(arch)
        
        # if arch == True:
        #     cv2.line(annotated_img,backplt1,backplt2,(0,128,0),6)
        # else:
        #     cv2.line(annotated_img,backplt1,backplt2,(0,0,128),6)
        #prints list of landmarks from 1 to 32 look at mediapipe diagram to know what landmark is which bodypart
        print(lmList)
        #the landmarks i want for side are 12 and 24 to get line and slope
        #plotting= detector.threeDimendionalplot(img)
        #print(world_lmList)
        head_x, head_y ,noseX, noseY, head_slope= detector.face_track(img,lmList)


        arch2= detector.checkback(img,(head_x,head_y),backplt2)
        
        cv2.line(annotated_img,(noseX,noseY),(head_x,head_y),(0,128,0),6)
        if arch2 == True:
            cv2.line(annotated_img,(head_x,head_y),backplt2,(0,128,0),6)
        else:
            cv2.line(annotated_img,(head_x,head_y),backplt2,(0,0,255),6)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        #resize is width than height
        resize = cv2.resize(annotated_img, (modded_width, constant_height))
        cv2.imshow("Image", resize)
        cv2.waitKey(1)  # millisecond delays
    return

if __name__ == "__main__":
    main()