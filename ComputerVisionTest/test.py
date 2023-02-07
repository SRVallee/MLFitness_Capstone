import numpy as np
import cv2
import mediapipe as mp
import PoseUtilities as pu
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


USE_CAM = True
# For static images:
# IMAGE_FILES = ["ComputerVisionTest/images/pushup.jpg"]
# BG_COLOR = (192, 192, 192) # gray
# with mp_holistic.Holistic(
#     static_image_mode=True,
#     model_complexity=2,
#     enable_segmentation=True,
#     refine_face_landmarks=True) as holistic:
#   for idx, file in enumerate(IMAGE_FILES):
#     image = cv2.imread(file)
#     image_height, image_width, _ = image.shape
#     # Convert the BGR image to RGB before processing.
#     results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # if results.pose_landmarks:
#     #   print(
#     #       f'Nose coordinates: ('
#     #       f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width}, '
#     #       f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height})'
#     #   )

#     annotated_image = image.copy()
#     # Draw segmentation on the image.
#     # To improve segmentation around boundaries, consider applying a joint
#     # bilateral filter to "results.segmentation_mask" with "image".
#     condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
#     bg_image = np.zeros(image.shape, dtype=np.uint8)
#     bg_image[:] = BG_COLOR
#     annotated_image = np.where(condition, annotated_image, bg_image)
#     # Draw pose, left and right hands, and face landmarks on the image.
#     mp_drawing.draw_landmarks(
#         annotated_image,
#         results.face_landmarks,
#         mp_holistic.FACEMESH_TESSELATION,
#         landmark_drawing_spec=None,
#         connection_drawing_spec=mp_drawing_styles
#         .get_default_face_mesh_tesselation_style())
#     mp_drawing.draw_landmarks(
#         annotated_image,
#         results.pose_landmarks,
#         mp_holistic.POSE_CONNECTIONS,
#         landmark_drawing_spec=mp_drawing_styles.
#         get_default_pose_landmarks_style())
#     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
#     # Plot pose world landmarks.
#     print(results.pose_world_landmarks.landmark[11])
#     mp_drawing.plot_landmarks(
#         results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)

# For webcam input:
cap = cv2.VideoCapture(0, apiPreference=cv2.CAP_ANY, params=[
  cv2.CAP_PROP_FRAME_WIDTH, 1920,
  cv2.CAP_PROP_FRAME_HEIGHT, 1080])
if not USE_CAM:
  cap = cv2.VideoCapture("ComputerVisionTest/videos/pushup.mp4")
  
  
f = open("landmarksLog.txt", 'w')

with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  
  frameNum = 0
  while cap.isOpened():
    frameNum += 1
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      if USE_CAM:
        continue
      else:
        break

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    # image = cv2.resize(image, (1280, 720))
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.namedWindow('MediaPipe Holistic', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('MediaPipe Holistic', 607, 1080)
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)
    landmarks = results.pose_world_landmarks
    angStr = 'None'
    angStr2 = 'None'
    if landmarks:
      # f.write('{' + str(frameNum) + ': ' + poseutil.frame_landmarks(landmarks) + '}\n')
      angs = pu.compute_body_angles(landmarks)
      angStr  = str(np.degrees(angs[4]))
      angStr2 = str(np.degrees(angs[5]))

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # mp_drawing.draw_landmarks(
    #     image,
    #     results.face_landmarks,
    #     mp_holistic.FACEMESH_CONTOURS,
    #     landmark_drawing_spec=None,
    #     connection_drawing_spec=mp_drawing_styles
    #     .get_default_face_mesh_contours_style())
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())
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
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
      
f.close()
cap.release()