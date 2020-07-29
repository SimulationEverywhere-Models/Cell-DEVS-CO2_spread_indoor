# Tools for image loading and analysis
# Thomas Roller

# Note that the Python module "Pillow" is required

import sys
from PIL import Image
from GeneralTools import GeneralTools

# Tools for handling images
class ImageTools:

    # Function: __init__
    # Purpose: prepare variables for image loading and analysis
    # Arguments:
    #     self: enclosing instance (automatic, not user specified)
    #     config: configuration file as a Python dictionary
    # Return:
    #     none
    def __init__ (self, config):
        self.colourTolerance = config["image"]["colourTolerance"]
        self.alphaTolerance = config["image"]["alphaTolerance"]
        self.colours = config["image"]["colours"]
        self.airColour = self.getAirColour()
        self.inputFile = config["files"]["input"]
        self.pixels = []
        self.width = self.length = 0
        self.randomGen = GeneralTools.RandomNumber(config["model"]["counter"]["seed"],
                                                   config["model"]["counter"]["minimum"],
                                                   config["model"]["counter"]["maximum"])

    # Get width of loaded image
    def getWidth (self):
        return self.width

    # Get length of loaded image
    def getLength (self):
        return self.length

    # Load the image
    # Function: load
    # Purpose: load the image specified in the configuration file
    # Arguments:
    #     self: enclosing instance (automatic, not user specified)
    #     debug: whether or not to show debug messages
    # Return:
    #     none
    def load (self, debug=False):
        try:
            image = Image.open(self.inputFile, "r")
        except FileNotFoundError:
            if (debug): print(f"ERROR: Could not load image file (\"{self.inputFile}\")")
            sys.exit(1)

        self.width, self.length = image.size
        self.pixels = list(image.getdata())

    # Function: correctColour
    # Purpose: correct colours that are not solid using the tolerance level from the configuration file
    # Arguments:
    #     self: enclosing instance (automatic, not user specified)
    #     pixel: the pixel (as a list of RGB and maybe alpha values)
    #     debug: whether or not to show debug messages
    # Return:
    #     none
    def correctColour (self, pixel, debug=False):
        pixel = list(pixel)
        for i in range(0, 3):  # only include RGB values (ignore alpha)
            if (abs(pixel[i]) <= self.colourTolerance):
                pixel[i] = 0
            elif (abs(pixel[i]) >= 255 - self.colourTolerance):
                pixel[i] = 255
            else:
                if (debug): print(f"| NOTE: Colour outside of tolerance (making loose estimate): {pixel}, colour {pixel[i]}")
                # Make rough guess
                if (pixel[i] < 255 / 2):
                    pixel[i] = 0
                else:
                    pixel[i] = 255
        return pixel

    # Get a string representation of the given pixel's colour
    # Function: getColourString
    # Purpose: 
    # Arguments:
    #     self: enclosing instance (automatic, not user specified)
    #     pixel: the pixel (as a list of RGB and maybe alpha values)
    #     debug: whether or not to show debug messages
    # Return:
    #     none
    def getColourString (self, pixel, debug=False):
        if (len(pixel) == 4 and pixel[3] <= self.alphaTolerance):  # Account for alpha
            if (debug): print(f"| NOTE: Transparent pixel (converting to colour of air cell): {pixel}")
            return self.airColour
        pixel = self.correctColour(pixel, debug=debug)
        for i in pixel:
            if (i != 0 and i != 255):
                return self.airColour
        return str(pixel[0]) + "," + str(pixel[1]) + "," + str(pixel[2])

    # Function: makeCells
    # Purpose: turn the image's pixels into cells
    # Arguments:
    #     self: enclosing intance (automatic, not user specified)
    #     debug: whether or not to show debug messages
    #     showProgress: whether or not to show progress messages
    # Return:
    #     list of cells
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
        return cells

    # Function: getColourProperties
    # Purpose: get the properties associated with the specified colour (designated in the configuration file)
    # Arguments:
    #     self: enclosing instance (automatic, not user specified)
    #     colour: the colour (as a string) being tested
    # Return:
    #     the properties of the given colour
    def getColourProperties (self, colour):
        try:
            return self.colours[colour]
        except KeyError:
            return self.colours[self.airColour]

    # Function: getAirColour
    # Purpose: get the colour of an air cell (designated in the configuration file)
    # Arguments:
    #     self: enclosing instance (automatic, not user specified)
    # Return:
    #     string representing the colour of an air cell
    def getAirColour (self):
        for colour in self.colours:
            if (self.colours[colour]["type"] == -100):  # If the colour corresponds to AIR
                return colour

    # Get the dimensions of an image without creating an ImageTools instance
    # Function: getDimensions
    # Purpose: get the dimensions of an image without creating an ImageTools instance
    # Arguments:
    #     filename: name of the image file to be checked
    #     debug: whether or not to show debug messages
    # Return:
    #     tuple representing the size of the image
    @staticmethod
    def getDimensions (filename, debug=False):
        try:
            return Image.open(filename, "r").size
        except:
            if (debug): print(f"ERROR: Could not load image file (\"{filename}\")")
            sys.exit(1)