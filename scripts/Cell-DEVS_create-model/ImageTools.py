# Tools for image loading and analysis
# Thomas Roller

# Note that the Python module "Pillow" is required

import sys
from PIL import Image
from GeneralTools import GeneralTools

# Tools for handling images
class ImageTools:

    # Prepare variables for image loading and analysis
    def __init__ (self, config):
        self.tolerance = config["image"]["tolerance"]
        self.colours = config["image"]["colours"]
        self.airColour = self.getAirColour()
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
        try:
            image = Image.open(self.inputFile, "r")
        except FileNotFoundError:
            print("ERROR: Could not load image file")
            sys.exit(1)

        self.width, self.length = image.size
        self.pixels = list(image.getdata())

    # Correct colours that are not solid using tolerance level
    def correctColour (self, pixel, debug=False):
        pixel = list(pixel)
        for i in range(0, len(pixel)):
            if (abs(pixel[i]) < self.tolerance):
                pixel[i] = 0
            elif (abs(pixel[i]) > self.tolerance):
                pixel[i] = 255
            else:
                if (debug): print(f"WARNING: correctColour: Unable to correct colour: {pixel}")
                # Make rough guess
                if (pixel[i] < 255 / 2):
                    pixel[i] = 0
                else:
                    pixel[i] = 255
        return pixel

    # Get a string representation of the given pixel's colour
    def getColourString (self, pixel, debug=False):
        pixel = self.correctColour(pixel, debug=debug)
        if (len(pixel) == 4 and pixel[3] == 0):  # Account for alpha
            print(f"NOTE: Transparent pixel: {pixel}")
            return self.airColour
        for i in pixel:
            if (i != 0 and i != 255):
                return self.airColour
        return str(pixel[0]) + "," + str(pixel[1]) + "," + str(pixel[2])

    # Turn the image's pixel's into cells
    def makeCells (self, debug=False, showProgress=False):
        maxStep = self.width * self.length
        cells = []
        for x in range (0, self.width):
            for y in range (0, self.length):
                if (showProgress):
                    currStep = ((x + 1) * self.length) + (y + 1)
                    GeneralTools.printProgress(currStep, maxStep)
                pixel = self.pixels[(self.width * y) + x]
                colour = self.getColourString(pixel, debug=debug)
                if (colour == self.airColour):
                    continue
                counter = self.getColourProperties(colour)["counter"]
                if (self.getColourProperties(colour)["type"] == -700):  # If the current cell is a WORKSTATION
                    counter = self.randomGen.getInt()
                cells.append(GeneralTools.makeCell(
                    [x, y],
                    self.getColourProperties(colour)["concentration"],
                    self.getColourProperties(colour)["type"],
                    counter
                ))
        print(f"makeCells: number of pixels: {len(self.pixels)}")
        print(f"makeCells: number of cells being returned: {len(cells)}")
        return cells

    # Get colour properties
    def getColourProperties (self, colour):
        try:
            return self.colours[colour]
        except KeyError:
            return self.colours[self.airColour]

    # Get the colour of air
    def getAirColour (self):
        for colour in self.colours:
            if (self.colours[colour]["type"] == -100):  # If the colour corresponds to white
                return colour

    # Get the dimensions of an image without creating an ImageTools instance
    @staticmethod
    def getDimensions (filename):
        try:
            return Image.open(filename, "r").size
        except:
            print("ERROR: Could not load image file")
            sys.exit(1)