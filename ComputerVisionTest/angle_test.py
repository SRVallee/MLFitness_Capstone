import PoseUtilities as pu
import numpy as np

i = np.array([-1, 0, 0])
j = np.array([0, -2, 0])
angleVec = np.array([-0.5, -1, 0])

print(np.degrees(pu.vector_angles(angleVec, i, j)))

i = np.array([-1, 0, 0])
j = np.array([0, -2, 0])
angleVec = np.array([-0.5, 0, -0.5])

print(np.degrees(pu.vector_angles(angleVec, i, j)))
