# General tools
# Thomas Roller

import math

class GeneralTools:

    # Function: makeCell
    # Purpose: create a cell with the given properties
    # Arguments:
    #     coords: a list of coordinates of the cell
    #     concentration: the concentration of the cell
    #     cellType: the type of the cell
    #     counter: the counter value of the cell
    # Return:
    #     the assembled cell
    @staticmethod
    def makeCell (coords, concentration, cellType, counter):
        return {
            "cell_id": coords,
            "state" : {
                "concentration" : concentration,
                "type" : cellType,
                "counter" : counter
            }
        }

    # Function: export
    # Purpose: export a string
    # Arguments:
    #     filename: name of the file to be used for exporting
    #     data: string to be exported
    # Return:
    #     none
    @staticmethod
    def export (filename, data):
        with open(filename, "w") as f:
            f.write(data)

    # Function: printProgress
    # Purpose: print a step of a progress indicator
    # Arguments:
    #     currStep: the current step
    #     maxStep: the maximum number of steps that can be preformed
    # Return:
    #     none
    @staticmethod
    def printProgress (currStep, maxStep):
        if (math.floor(currStep % (maxStep / 100)) == 0):
            progress = round((currStep / maxStep) * 100)
            print(f"| Progress: {min(progress, 100)}%   \r", end="")

    # Class for generating replicable psuedorandom numbers
    class RandomNumber:

        # Function: __init__
        # Purpose: initialize an instance of RandomNumber
        # Arguments:
        #     self: enclosing instance (automatic, not user specified)
        #     seed: an integer to seed the random number generation
        #     minimum: the minimum possible value that can be generated
        #     maximum: the maximum possible value that can be generated
        #     internalLimit: a value that limits how large numbers are able to become (may conflict with maximum value)
        # Return:
        #     none
        def __init__ (self, seed, minimum, maximum, internalLimit=1000):
            self.value = int(seed)
            self.maximum = int(maximum)
            self.minimum = int(minimum)
            self.counter = 0
            self.internalLimit = int(internalLimit)

        # Function: getInt
        # Purpose: get the next random number and progress generator
        # Arguments:
        #     self: enclosing instance (automatic, not user specified)
        # Return:
        #     pseudorandom integer
        def getInt (self):
            self.value = ((self.value ** self.value) + self.counter) % self.internalLimit  # Generate next value, keep within reasonable limits
            self.counter += 1
            return self.minimum + (self.value  % ((self.maximum + 1) - self.minimum))  # Bring the value within permitted range