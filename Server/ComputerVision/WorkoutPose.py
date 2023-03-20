import statistics
class WorkoutPose:

    def __init__(self, angles : list, stdv = None, numberOfReps = None):
        self._angles = angles
        self._stdv = stdv
        self._reps = numberOfReps


    def compareTo(self, anotherPose):
        diff = 0
        for i in range(len(self._angles)):
            diff += abs(self._angles[i] - anotherPose.getAngles()[i])

        return diff


    def getAngles(self):
        return self._angles

    def setAngles(self, newAngles):
        self._angles = newAngles

    def getAngle(self, index: int):
        return self._angles[index]

    def setAngle(self, newAngle, index : int):
        self._angles[index] = newAngle

    def getStdv(self):
        return self._stdv

    def setStdv(self, stdv):
        self._stdv = stdv

    def getStdvSingle(self, index : int):
        return self._stdv[index]


    def getPopulationNumber(self):
        if self._reps:
            return self._reps
        
        return 1

    def plusPopulation(self, n : int):
        self._reps += n


    def toList(self):
        return [self._angles, self._stdv, self._reps]

    def evaluatePose(self, other):
        accuracies = []
        for i in len(self._angles):
            deviation = abs(self._angles[i] - other.getAngle(i))/self.getStdvSingle(i)

            if  deviation >= 1:
                accuracies.append(0)
            else:
                accuracies.append((1-deviation)*100)

            
        
        return statistics.mean(accuracies), min(accuracies)

    