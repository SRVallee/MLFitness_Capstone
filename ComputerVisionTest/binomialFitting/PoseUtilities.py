import numpy as np
import json

"""
   y
   |
   |_______ x
  /
 /
z
"""

class Point:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z


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

ANGLE_ARRAY = np.array([
    [11, 12, 23, 13], # left shoulder
    [23, 11, 24, 25], # left hip
    [12, 11, 24, 14], # right shoulder
    [24, 12, 23, 26], # right hip
    [13, 11, 15, -1], # left elbow
    [25, 23, 27, -1], # left knee
    [14, 12, 16, -1], # right elbow
    [26, 24, 28, -1]  # right knee
])

COMPLEX_ANGLE_ARRAY = np.array([
    [11, 12, 23, 24,  7,  8], # head angle 
    [23, 24, 27, 28, 11, 12] # body angle 
    
])

def arrange_frame_cols(isPos, angles):
    
    cols = angles[0].copy().tolist()
    cols.extend(angles[len(angles)-1])
    cols.extend(angles[0])
    
    if isPos:
        cols.append(1)
    else:
        cols.append(0)
    
    return cols

def frame_landmarks_json(landmarks):
    """ Get json of single frame of landmarks.

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

def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        
    return data

def frame_landmarks_csv(index, landmarks, isGood):
    
    
    return

def vectorize(landmarkA, landmarkB):
    """Turn Lankmarks into vector for numpy from A -> B

    Args:
        landmarkA (pose_world_landmark): landmark from blazepose
        landmarkB (pose_world_landmark): landmark from blazepose
    """
    
    return np.array([landmarkB.x - landmarkA.x, 
                     landmarkB.y  - landmarkA.y,
                     landmarkB.z  - landmarkA.z])

def unit_vectorize(vector):
    """ Returns the unit vector of a vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(vecA, vecB):
    unitA = unit_vectorize(vecA)
    unitB = unit_vectorize(vecB)
    return np.arccos(np.clip(np.dot(unitA, unitB), -1.0, 1.0))

def midpoint(landmarkA, landmarkB):
    return Point((landmarkB.x + landmarkA.x)/2, 
                 (landmarkB.y + landmarkA.y)/2, 
                 (landmarkB.z + landmarkA.z)/2)

def vector_angles(angleVec, vecI, vecJ, right=0):
    # Compute both angles of a vec to projected onto the plane I,K and I,J
    # I should be horizontal and J should be vertical relative to the 2-axis rotation
    # for right shoulder we will say (11,12) is vector I, (12, 24) is vector J,
    # vector K is what the angle is being taken from
    
    normIJ = np.cross(vecI, vecJ)    # First have to find normal of I,J -> K
    normIK = np.cross(vecI, normIJ)  # normal of I,K 
    
    magnitudeIJ = np.linalg.norm(normIJ) # plane I,J normal magnitude
    magnitudeIK = np.linalg.norm(normIK) # plane I,K normal magnitude
    
    # Compute projection of angleVec onto I,K plane
    
    # project angle vector onto plane IJ normal
    projIJNormal = (np.dot(angleVec, normIJ)/magnitudeIJ**2)*normIJ 
    # project angle vector onto plane IK normal
    projIKNormal = (np.dot(angleVec, normIK)/magnitudeIK**2)*normIK 
    
    # print(normIJ/magnitudeIJ, normIK/magnitudeIK)
    
    # Subtract projection of angle vec onto IJ normal to find projection onto plane
    projIJ = angleVec - projIJNormal 
    # Subtract projection of angle vec onto IK normal to find projection onto plane
    projIK = angleVec - projIKNormal 
    
    # Compute angle between Vec J and angleVec projection
    threshold = 0.01
    if np.linalg.norm(projIJ) > threshold: # if projection passes threshold
        angleJ = angle_between(projIJ, vecJ)
    else:
        angleJ = 0
        
    # Compute angle between Vec I and angleVec projection
    if np.linalg.norm(projIK) > threshold: # if projection passes threshold
        angleI = angle_between(projIK, vecI)
    else:
        angleI = 0
    
    return angleI, angleJ

def compute_body_angles(landmarks):
    angleArr = np.zeros(16)
    # head and body
    j = 0
    for i in range(2):
        centre = midpoint(landmarks.landmark[COMPLEX_ANGLE_ARRAY[i, 0]], 
                           landmarks.landmark[COMPLEX_ANGLE_ARRAY[i, 1]])
        pointI = landmarks.landmark[COMPLEX_ANGLE_ARRAY[i, 0]]
        pointJ = midpoint(landmarks.landmark[COMPLEX_ANGLE_ARRAY[i, 2]], 
                           landmarks.landmark[COMPLEX_ANGLE_ARRAY[i, 3]])
        pointK = midpoint(landmarks.landmark[COMPLEX_ANGLE_ARRAY[i, 4]], 
                           landmarks.landmark[COMPLEX_ANGLE_ARRAY[i, 5]])
        vecK = vectorize(centre, pointK)
        vecI = vectorize(centre, pointI)
        vecJ = vectorize(centre, pointJ)
        
        lrAngle, fbAngle = vector_angles(vecK, vecI, vecJ)
        
        angleArr[j] = lrAngle
        angleArr[j+1] = fbAngle
        j += 2
        
    # shoulders, hips
    for i in range(8):
        centre = landmarks.landmark[ANGLE_ARRAY[i, 0]]
        pointI = landmarks.landmark[ANGLE_ARRAY[i, 1]]
        pointJ = landmarks.landmark[ANGLE_ARRAY[i, 2]]
        pointK = landmarks.landmark[ANGLE_ARRAY[i, 3]]
        if i < 4: # shoulders and hips
            vecK = vectorize(centre, pointK)
            vecI = vectorize(centre, pointI)
            vecJ = vectorize(centre, pointJ)
            
            angle, angle2 = vector_angles(vecK, vecI, vecJ)
            angleArr[j] = angle
            angleArr[j+1] = angle2
            j += 2
        else:     # elbows and knees
            angle = angle_between(vectorize(centre, pointI), vectorize(centre, pointJ))
            angleArr[j] = angle
            j += 1
            
    # for i in range(1,12):
    #     if i != 4 & i != 5 & i != 7:
    #         angleArr[i] = np.pi - angleArr
    return angleArr

def compute_body_ang(landmarks):
    angleArr = np.zeros(24)
    # -- Head --
    j = 0
    shoulders = midpoint(landmarks.landmark[COMPLEX_ANGLE_ARRAY[0, 0]], 
                        landmarks.landmark[COMPLEX_ANGLE_ARRAY[0, 1]])
    pointI = landmarks.landmark[COMPLEX_ANGLE_ARRAY[0, 0]]
    pointJ = midpoint(landmarks.landmark[COMPLEX_ANGLE_ARRAY[0, 2]], 
                        landmarks.landmark[COMPLEX_ANGLE_ARRAY[0, 3]])
    head = midpoint(landmarks.landmark[COMPLEX_ANGLE_ARRAY[0, 4]], 
                        landmarks.landmark[COMPLEX_ANGLE_ARRAY[0, 5]])
    angle, angle2 = vector_angles(
        vectorize(shoulders, head),
        vectorize(shoulders, pointI),
        vectorize(shoulders, pointJ)
    )
    angleArr[j] = angle
    angleArr[j+1] = angle2
    j += 2
    
    # -- Body -- 
    
    return