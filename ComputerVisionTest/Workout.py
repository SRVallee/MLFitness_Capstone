from WorkoutPose import WorkoutPose
import UpdateStats
import json
class Workout:
    def __init__(self, model : list = None) -> None:
        if model:
            self._top = WorkoutPose(model["Top"][0], model["Top"][1], model["Top"][2])
            self._bottom = WorkoutPose(model["Top"][0], model["Top"][1], model["Top"][2])
            self._impAng = model["ImportantAngles"]

    def loadModel(self, path):
        with open(path, "r") as f:
            model = json.load(f)
        self._top = WorkoutPose(model["Top"][0], model["Top"][1], model["Top"][2])
        self._bottom = WorkoutPose(model["Top"][0], model["Top"][1], model["Top"][2])
        self._impAng = model["ImportantAngles"]
        return self
            
    def updateModel(self, newPose : WorkoutPose, poseType : str):
        if poseType == "Top":
            newAngles = self._top.getAngles()
            for i in len(newAngles):
                newAngle = UpdateStats.update_average_with_one_value(
                    newAngles[i], 
                    self._top.getPopulationNumber(), 
                    newPose.getAngles()[i])
                newAngles[i] = newAngle

            self._top.setAngles(newAngles)
            self._top.plusPopulation(1)
                    
        elif poseType == "Bottom":
            newAngles = self._bottom.getAngles()
            for i in len(newAngles):
                newAngle = UpdateStats.update_average_with_one_value(
                    newAngles[i], 
                    self._bottom.getPopulationNumber(), 
                    newPose.getAngles()[i]
                )

                newStdv = UpdateStats.update_stdev(
                    newAngles[i],
                    self._bottom.getStdv()[i],
                    self._bottom.getPopulationNumber(),
                    newPose.getAngles()[i]
                )
                newAngles[i] = newAngle
                
            self._bottom.setAngles(newAngles)
            self._bottom.setStdv(newStdv)
            self._bottom.plusPopulation(1)

    def saveModel(self, path):
        model = {"Top": self._top.toList(), "Bottom": self._bottom, "ImportantAngles": self._impAng}
        with open(path, "w") as f:
            json.dump(model, f)

    def getTop(self):
        return self._top

    def getBottom(self):
        return self._bottom

    def compareToTop(self, other : WorkoutPose):
        return self._top.compareTo(other)
        
    def chooseClosestTop(self, other1, other2):
        if (self.compareToTop(other1) > self.compareToTop(other2)):
            return other2
        else:
            return other1

    def compareToBottom(self, other : WorkoutPose):
        return self._top.compareTo(other)
        
    def chooseClosestBottom(self, other1, other2):
        if (self.compareToBottom(other1) > self.compareToBottom(other2)):
            return other2
        else:
            return other1

    def getImportantAngles(self):
        return self._impAng