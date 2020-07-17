# Tools for image loading and analysis
# Written by Thomas Roller

# Note that the Python module "Pillow" is required

from PIL import Image
from GeneralTools import GeneralTools

# Tools for handling images
class ImageTools:

    # Prepare variables for image loading and analysis
    def __init__ (self, config):
        self.tolerance = config["image"]["tolerance"]
        self.colours = config["image"]["colours"]
        self.inputFile = config["files"]["input"]
        self.pixels = []
        self.width = self.length = 0
        self.randomGen = GeneralTools.RandomNumber(config["model"]["counter"]["seed"],
                                                   config["model"]["counter"]["minimum"],
                                                   config["model"]["counter"]["maximum"])

    def getWidth (self):
        return self.width

    def getLength (self):
        return self.length

    # Load the image
    def load (self):
        image = Image.open(self.inputFile, "r")
        self.width, self.length = image.size
        self.pixels = list(image.getdata())

    # Correct colours that are not solid using tolerance level
    def correctColour (self, pixel):
        pixel = list(pixel)
        for i in range(0, len(pixel)):
            if (abs(pixel[i]) < self.tolerance):
                pixel[i] = 0
            elif (abs(pixel[i]) > self.tolerance):
                pixel[i] = 255
            else:
                print("correctColour: Unable to correct colour: {0}".format(pixel))
        return pixel

    # Get a string representation of the given pixel's colour
    def getColourString (self, pixel):
        pixel = self.correctColour(pixel)
        for i in pixel:
            if (i != 0 and i != 255):
                return "255,255,255"
        return str(pixel[0]) + "," + str(pixel[1]) + "," + str(pixel[2])

    # Turn the image's pixel's into cells
    def makeCells (self):
        cells = []
        for x in range (0, self.width):
            for y in range (0, self.length):
                pixel = self.pixels[(self.width * y) + x]
                colour = self.getColourString(pixel)
                if (colour == "255,255,255"):
                    continue
                counter = self.colours[colour]["counter"]
                if (self.colours[colour]["type"] == -700):  # If the current cell is a WORKSTATION
                    counter = self.randomGen.getInt()
                cells.append(GeneralTools.makeCell(
                    [x, y],
                    self.colours[colour]["concentration"],
                    self.colours[colour]["type"],
                    counter
                ))
        return cells