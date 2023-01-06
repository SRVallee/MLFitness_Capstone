import time

import cv2
import mediapipe as mp

#this is just the class to find and create the pose
class poseDetector():

    def __init__(self, mode=False,modcomp = 1, smooth=True,segmen=False, smoothseg=True,
                 detectionCon=0.5, trackCon=0.5):

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
        #print(results.pose_landmarks) print all landmarks aka points every frame

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS) #landmarks are for the dots on the body there are 32 dots i believe
        return img

    #this will be used to get each position of each landmark and label them
    def findPosition(self,img, draw=True):
        lmList =[] #landmark list
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape # we need this because
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h) #this gives the pixel point of the landmarks
                lmList.append([id,cx,cy])
                #if found checks if can draw it if can draw
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)#this will over lay on points if seeing properly it would be blue
        return lmList

def main():
    cap = cv2.VideoCapture('ComputerVisionTest/videos/pushup.mp4')  # the video
    pTime = 0
    detector = poseDetector()
    while True:
        #this sees if it can read the frame that it is given
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        #prints list of landmarks from 1 to 32 look at mediapipe diagram to know what landmark is which bodypart
        print(lmList)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)  # millisecond delays

if __name__ == "__main__":
    main()