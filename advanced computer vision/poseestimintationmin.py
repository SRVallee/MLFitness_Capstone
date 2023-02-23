import time

import cv2
import mediapipe as mp


mpDraw = mp.solutions.drawing_utils #this is for drawing everything
mpPose = mp.solutions.pose # this is for a model
pose = mpPose.Pose() # this is for determining pose of person

cap = cv2.VideoCapture('runningman.mp4') #the video
pTime = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    #print(results.pose_landmarks) print all landmarks aka points every frame
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) #landmarks are for the dots on the body there are 32 dots i believe
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape # we need this because
            print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h) #this gives the pixel point of the landmarks
            cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)#this will over lay on points if seeing properly it would be blue
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1) # millisecond delays

