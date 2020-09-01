# Class which controls the flow of the program
# Thomas Roller

import sys
import json
from ImageTools import ImageTools
from ConvertTools import ConvertTools
from GeneralTools import GeneralTools

class Control:

    # Function: start
    # Purpose: entry point of Control object
    # Arguments:
    #     args: arguments given by the argparse module
    # Return:
    #     none
    @staticmethod
    def start (args):
        configFile = args.config

        config = ""
        try:
            # Load configuration from file
            with open(configFile, "r") as f:
                config = f.read()
        except FileNotFoundError:
            print("ERROR: Could not load configuation file")
            sys.exit(1)

        # Prepare command line arguments for later use
        debug = args.prog_msg
        imgMsg = args.img_msg
        critMsg = not args.no_crit_msg

        config = json.loads(config)  # Convert JSON string into dictionary

        # Ensure the types of files given are valid
        convertType = Control.convertType(config["files"], args.dim, critMsg=critMsg)
        if (convertType is None and critMsg):
            print("ERROR: Invalid file extension")
            sys.exit(1)

        model = None
        # Input model is an image with matching dimensions
        if (convertType == "exact_image"):
            model = Control.process_image(config, debug=debug, imgMsg=imgMsg)
        # Input model is an image with mismatched dimensions (guessing required)
        elif (convertType == "interpolate_image"):
            model = Control.process_image(config, outDim=args.dim, debug=debug, imgMsg=imgMsg)
        # Input model is a JSON
        elif (convertType == "json"):
            model = Control.process_json_2Dto3D(config)

        # Export the JSON string
        if (debug): print("Exporting data to file...")
        GeneralTools.export(config["files"]["output"], ConvertTools.getString(model))

    # Function: getExtension
    # Purpose: get the extension of a file
    # Arguments:
    #     filename: name of the file being checked
    # Return:
    #     the file's extension (lowercase)
    @staticmethod
    def getExtension (filename):
        loc = filename.find(".")
        if (loc < 0 or loc >= len(filename) - 1):
            return None
        return filename[loc + 1:].lower()

    # Function: convertType
    # Purpose: determine what type of conversion to preform (image-to-JSON, JSON-to-JSON, etc.)
    # Arguments:
    #     files: input/output files from the configuration file
    #     outDim: the desired dimensions of the end result
    #     critMsg: whether or not to show critical messages
    # Return:
    #     conversion type identifier
    @staticmethod
    def convertType (files, outDim=None, critMsg=False):
        imageFormats = ["bmp", "jpg", "jpeg", "png"]
        extension = Control.getExtension(files["input"])
        # If there is no extension
        if (extension is None):
            return None
        # If the extension indicates an image
        elif (extension in imageFormats):
            imageDim = ImageTools.getDimensions(files["input"], debug=critMsg)
            # If the user did not provide a specific output dimension (no error due to short-circuit evaluation)
            if (outDim == None or (imageDim[0] == outDim[0] and imageDim[1] == outDim[1])):
                return "exact_image"
            # If the user provided a specific output dimension
            else:
                return "interpolate_image"
        # If the extension indicates a JSON
        elif (extension == "json"):
            return "json"

    # Function: process_image
    # Purpose: convert image files to 2D or 3D formatted models (depending on configuration file)
    # Arguments:
    #     config: the configuration file as a Python dictionary
    #     outDim: the desired dimensions of the end result
    #     debug: whether or not to show debug messages
    #     imgMsg: whether or not to show image/colour related messages
    #     critMsg: whether or not to show critical messages
    # Return:
    #     final scenario as a Python dictionary
    @staticmethod
    def process_image (config, outDim=None, debug=False, imgMsg=False, critMsg=False):
        if (debug): print("Preparing tools...")
        image = ImageTools(config)  # Prepare the image tools
        if (debug): print("Loading image...")
        image.load(critMsg)         # Load the image
        if (debug): print("Making cells...")
        cells = image.makeCells(debug=imgMsg, showProgress=debug)  # Make cells out of the image

        width, length = image.getWidth(), image.getLength()

        # If scaling is required
        if (outDim is not None):
            if (debug): print("NOTE: Image dimensions do not match provided dimensions (inexact image interpolation will take place)")
            if (debug): print("Scaling cells...")
            cells = ConvertTools.scaleCells(cells, [width, length], outDim, debug=debug, critMsg=critMsg)
            width, length = outDim

        # Generate the head of the model
        head = ConvertTools.createHead(width, length, config["model"])

        # If the model is 3D, extend the walls and add a floor and ceiling
        if (config["model"]["height"] > 1):
            if (debug):print("Extending cells...")
            cells = ConvertTools.getExtendedCells(config["model"], cells)
            if (debug): print("Adding floor and ceiling...")
            cells = ConvertTools.addFloorCeiling(width, length, config["model"]["height"], cells, showProgress=debug)

        return ConvertTools.createStructure(head, cells)  # Combine the head and the cells

    # Function: process_json_2Dto3D
    # Purpose: convert 2D JSON formatted scenarios to 3D JSON formatted scenarios
    # Arguments:
    #     config: the configuration file as a Python dictionary
    #     critMsg: whether or not to show critical messages
    # Return:
    #     final scenario as a Python dictionary
    @staticmethod
    def process_json_2Dto3D (config, critMsg=False):
        # Get 2D JSON
        data = ""
        inputFile = config["files"]["input"]
        try:
            # Load configuration from file
            with open(inputFile, "r") as f:
                data = f.read()
        except FileNotFoundError:
            if (critMsg): print(f"ERROR: Could not load input file {inputFile}")
            sys.exit(1)

        data = json.loads(data)  # Convert JSON string into dictionary

        width, length = data["scenario"]["shape"][0], data["scenario"]["shape"][1]

        # Generate the head of the model
        head = ConvertTools.createHead(width, length, config["model"])

        # Extract the cells
        cells = data["cells"]

        # If the model is 3D, extend the walls and add a floor and ceiling
        if (config["model"]["height"] > 1):
            cells = ConvertTools.getExtendedCells(config["model"], cells)
            cells = ConvertTools.addFloorCeiling(width, length, config["model"]["height"], cells)

        return ConvertTools.createStructure(head, cells)  # Combine the head and the cells