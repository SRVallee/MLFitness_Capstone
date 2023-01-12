import numpy
import json

KEYPOINT_DICT = {
    10 : 'nose',  # real nose landmark number is 0. Using as stand-in for head
    11 : 'left_shoulder',
    12 : 'right_shoulder',
    13 : 'left_elbow',
    14 : 'right_elbow',
    15 : 'left_wrist',
    16 : 'right_wrist',
    17 : 'left_pinky',
    18 : 'right_pinky',
    19 : 'left_index',
    20 : 'right_index',
    21 : 'left_thumb',
    22 : 'right_thumb',
    23 : 'left_hip',
    24 : 'right_hip',
    25 : 'left_knee',
    26 : 'right_knee',
    27 : 'left_ankle',
    28 : 'right_ankle', 
    29 : 'left_heel', 
    30 : 'right_heel', 
    31 : 'left_foot_index',
    32 : 'right_foot_index'
}

def frame_landmarks(landmarks):
    """get json of single frame of landmarks

    Args:
        landmarks (results.pose(_world)_landmarks): landmarks

    Returns:
        String: single frame's landmarks in json
    """
    
    dict = {}
    for i in range(10,32):
        x = 0
        y = 0
        z = 0
        if i == 10:
            x = landmarks.landmark[0].x
            y = landmarks.landmark[0].y 
            z = landmarks.landmark[0].z
        else:
            x = landmarks.landmark[i].x
            y = landmarks.landmark[i].y
            z = landmarks.landmark[i].z
            
        dict[KEYPOINT_DICT[i]] = {'x' : x, 'y' : y, 'z' : z}

    return json.dumps(dict)