# Class which controls the flow of the program
# Thomas Roller

import sys
import json
from ImageTools import ImageTools
from ConvertTools import ConvertTools
from GeneralTools import GeneralTools

class Control:

    @staticmethod
    def start (argv):
        # Get configuration filename
        configFile = "config.json"
        if (len(argv) == 2):
            configFile = argv[1]

        config = ""
        try:
            # Load configuration from file
            with open(configFile, "r") as f:
                config = f.read()
        except FileNotFoundError:
            print("ERROR: Could not load configuation file")
            sys.exit(1)

        config = json.loads(config)  # Convert JSON string into dictionary

        # Will branch when more functionality is added
        model = None
        if (True):
            model = Control.exactImageParse(config)

        # Export the JSON string
        GeneralTools.export(config["files"]["output"], ConvertTools.getString(model))

    @staticmethod
    def exactImageParse (config):
        image = ImageTools(config)  # Prepare the image tools
        image.load()                # Load the image
        cells = image.makeCells()   # Make cells out of the image

        # Generate the head of the model
        head = ConvertTools.createHead(image.getWidth(), image.getLength(), config["model"])

        # If the model is 3D, extend the walls and add a floor and ceiling
        if (config["model"]["height"] > 1):
            cells = ConvertTools.getExtendedCells(config["model"], cells)
            cells = ConvertTools.addFloorCeiling(image.getWidth(), image.getLength(), config["model"]["height"], cells)

        return ConvertTools.createStructure(head, cells)  # Combine the head and the cells