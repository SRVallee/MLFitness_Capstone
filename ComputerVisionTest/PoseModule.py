import cv2
import mediapipe as mp
import numpy as np
import binomialFitting.PoseUtilities as pu
import binomialFitting.KeyframeExtraction as KeyframeExtraction
import machineLearning.MachineLearningInitial as mli
import mp_drawing_modified
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

VIEW_IMAGE = False
VIEW_VIDEO = True

# For static images:
if VIEW_IMAGE:
    IMAGE_FILES = ["ComputerVisionTest/images/pushup.jpg"]
    BG_COLOR = (192, 192, 192) # gray
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5) as pose:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.pose_landmarks:
                continue
            print(
                f'Nose coordinates: ('
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].z})'
            )

            print(results.pose_world_landmarks.landmark[11])
            print(KeyframeExtraction.getAngle(results, 14, "x"))
            
            annotated_image = image.copy()
            # Draw segmentation on the image.
            # To improve segmentation around boundaries, consider applying a joint
            # bilateral filter to "results.segmentation_mask" with "image".
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            annotated_image = np.where(condition, annotated_image, bg_image)
            # Draw pose landmarks on the image.
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
            # Plot pose world landmarks.
            # mp_drawing.plot_landmarks(
            #     results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

# For webcam input:
if VIEW_VIDEO:
    path ="C:/Users/1234c/Documents/School/CMPT496/vids/"
    vids = ["good-01.mp4", "good-02.mp4", "good-03.mp4", "good-04.mp4",
            "good-05.mp4", "good-06.mp4", "good-07.mp4", "good-08.mp4",
            "good-09.mp4", "bad-10.mp4" , "bad-11.mp4" , "bad-12.mp4" ,
            "bad-13.mp4" , "bad-14.mp4" , "bad-15.mp4" , "bad-16.mp4" ,
            "bad-17.mp4" , "good-18.mp4", "good-19.mp4", "good-20.mp4",
            "good-21.mp4", "good-22.mp4", "good-23.mp4", "good-24.mp4",
            "good-25.mp4", "good-26.mp4", "good-27.mp4", "good-28.mp4",]
    breakFlag = False
    
    data = []
    
    for i in range(len(vids)):
        status_str = vids[i].split('-')[0]
        classifierPositive = (status_str == "good")
        
        cap = cv2.VideoCapture(path + vids[i])
        cap.set(cv2.CAP_PROP_FPS, 120)
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
                cv2.namedWindow('ML Test', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('ML Test', 607, 1080)
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                landmarks = results.pose_world_landmarks
                angStr = 'None'
                angStr2 = 'None'
                if landmarks:
                    # f.write('{' + str(frameNum) + ': ' + poseutil.frame_landmarks(landmarks) + '}\n')
                    angs = pu.compute_body_angles(landmarks)
                    # print(angs)
                    angStr  = str(np.degrees(angs[13]))
                    angStr2 = str(np.degrees(angs[15]))
                allFrames.append(results)
                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                # Flip the image horizontally for a selfie-view display.
                cv2.flip(image, 1)
                image = cv2.putText(image, angStr, 
                          (0, 130), 
                          cv2.FONT_HERSHEY_PLAIN,
                          10,
                          (255,255,10),
                          2,
                          cv2.LINE_AA)
                image = cv2.putText(image, angStr2, 
                          (0, 260), 
                          cv2.FONT_HERSHEY_PLAIN,
                          10,
                          (255,255,10),
                          2,
                          cv2.LINE_AA)
                cv2.imshow('ML Test', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    breakFlag = True
                    break
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        rSquared = 0.1
        
        print(f"File: {vids[i]}")
        extracted, angs = KeyframeExtraction.extractFrames(allFrames, rSquared, True)
        print(f"{len(extracted)} frames extracted")
        if len(extracted) > 2:
            print(f"frames: {len(allFrames)} framerate: {fps}")
            print(f"RSquared: {rSquared}")
            print(extracted)
            n = input("Frame to display: ")
            while n != "no":
                
                n = int(n)-1
                mp_drawing_modified.plot_landmarks(extracted[n][0].pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
                n = input("Frame to display: ")
        
        data.append(pu.arrange_frame_cols(classifierPositive, angs))
        
        if breakFlag:
            break
        
    # if not breakFlag:
        # mli.do_ml(data)
        