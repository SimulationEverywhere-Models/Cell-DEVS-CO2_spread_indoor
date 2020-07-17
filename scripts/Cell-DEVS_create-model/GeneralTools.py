# General tools
# Written by Thomas Roller

class GeneralTools:

    # Creates and retruns an IMPERMEABLE_STRUCTURE cell with the given coordinates
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

    # Export a string
    @staticmethod
    def export (filename, data):
        with open(filename, "w") as f:
            f.write(data)

    # Class for generating psuedorandom numbers
    class RandomNumber:

        def __init__ (self, seed, minimum, maximum, internalLimit=1000):
            self.value = seed
            self.maximum = maximum
            self.minimum = minimum
            self.counter = 0
            self.internalLimit = internalLimit

        # Get the next random number and progress generator
        def getInt (self):
            self.value = ((self.value ** self.value) + self.counter) % self.internalLimit  # Generate next value, keep within reasonable limits
            self.counter += 1
            return self.minimum + (self.value  % ((self.maximum + 1) - self.minimum))  # Bring the value within permitted range