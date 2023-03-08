import cv2
import numpy as np
import sys

# Load the video
videoname = "/motioncapture/Correct_squat/SquatV1side.mp4"
video = cv2.VideoCapture(sys.path[0]+ videoname)  # the video sys.path[0] is the current path of the file
constant_height = 700
# Get the frame count
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Preprocess the frames
frames = []
for i in range(frame_count):
    ret, frame = video.read()
    if not ret:
        break
    frame = cv2.resize(frame, (224, 224))
    frames.append(frame)
    height = frame.shape[0]
    width = frame.shape[1]
    height_percentage = float(constant_height/int(height))
    modded_width = int(float(width)*height_percentage)

# Calculate the body pose difference
pose_diff = []
for i in range(1, frame_count):
    frame1 = frames[i-1]
    frame2 = frames[i]
    diff = np.abs(frame1 - frame2).mean()
    pose_diff.append(diff)

# Select the key frames
key_frames = []

threshold = np.mean(pose_diff) + 2 * np.std(pose_diff)
for i, diff in enumerate(pose_diff):
    if diff > threshold:
        key_frames.append(i)
print(key_frames)
video.set(cv2.CAP_PROP_POS_FRAMES,82)
ret, frame = video.read()
resize = cv2.resize(frame, (modded_width, constant_height))
cv2.imshow("image",resize)
cv2.waitKey(10000)
# Release the video
video.release()