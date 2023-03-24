import cv2
import mediapipe as mp
from pathlib import Path
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Extract human 3D poses from videos using BlazePose model.')

parser.add_argument('input_video', type=str, help='input video')
parser.add_argument('-o', type=str, action='store', required=False,
                    help='output frames directory (will be created if does not exist)')
parser.add_argument('-v', type=bool, required=False, const=True, nargs='?', default=False, help='show verbose output')

args = parser.parse_args()

video_path = Path(args.input_video)
video_name = video_path.stem
verbose = args.v

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def landmarks_to_vex_array(landmarks):
    arr = ''

    for idx, i in enumerate(landmarks):
        arr = arr + '{' + f'{i.x},{i.y},{i.z}' + '}'

        if idx < len(landmarks) - 1:
            arr += ','

    return arr


cap = cv2.VideoCapture(sys.path[0]+'/motioncapture/SquatV1angle.mp4')

frame = 0
max_frames = 5000
res = ''

with mp_pose.Pose(
        min_detection_confidence=0.75,
        min_tracking_confidence=0.6) as pose:

    while cap.isOpened():
        success, image = cap.read()

        if not success:
            break

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Save calculated coordinates into files
        if args.o:
            output_dir = Path(args.o)

            if hasattr(results.pose_world_landmarks, 'landmark'):
                landmarks = results.pose_world_landmarks.landmark

                frame_path = output_dir / str(frame)

                output_dir.mkdir(parents=True, exist_ok=True)

                with open(frame_path, 'a') as output_file:
                    
                    if (verbose):
                      print('Saving frame to', frame_path)
                    
                    for idx, i in enumerate(landmarks):
                        line = f'{i.x},{i.y},{i.z}'
                        output_file.write(f'{line}\n')

                if frame > max_frames:
                    break

            frame += 1
        else:
            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

cap.release()
