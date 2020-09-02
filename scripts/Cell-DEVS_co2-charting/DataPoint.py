# Carleton University (ARSLab)
# Thomas Roller

# Class: DataPoint
# Purpose: pair information for a specific time-step's concentration with the time
# Arguments:
#     self: enclosing instance (automatic, not user specified)
#     time: the time-step the DataPoint will represent
#     conc: the concentration of the DataPoint at a specific time-step
class DataPoint:

    # Constructor for the DataPoint class
    def __init__ (self, time, conc):
        self.time = time
        self.conc = conc

    # Get the time-step that the DataPoint represents
    def getTime (self):
        return self.time

    # Get the concentration of the time-step
    def getConcentration (self):
        return self.conc

    # Create a copy of the DataPoint
    def copy (self):
        return DataPoint(self.time, self.conc)

    # Create a list that represents the DataPoint
    def toArray (self):
        return [self.time, self.conc]

    # Provide a string representation of the DataPoint
    def __str__ (self):
        return f"{self.time}:{self.conc}"

    # Provide a way to compare DataPoints (based on concentration)
    def __lt__ (self, value):
        return self.conc < value.conc

    # Provide a way to compare DataPoints (based on time)
    def __eq__ (self, value):
        return self.time == value.time  # not concerned about concentration

    # Provide a way to compare DataPoints
    def __ne__ (self, value):
        return not self.__eq__(value)