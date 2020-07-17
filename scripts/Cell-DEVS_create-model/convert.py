# Script to convert image files into models (2D and 3D)
# Written by Thomas Roller

import sys
import json
from ImageTools import ImageTools
from ConvertTools import ConvertTools
from GeneralTools import GeneralTools

# Check for proper usage
if (len(sys.argv) != 1 and len(sys.argv) != 2):
    print("Usage: python3 convertImage.py [<config file>]")
    sys.exit(0)

# Get configuration filename
configFile = "config.json"
if (len(sys.argv) == 2):
    configFile = sys.argv[1]

config = ""
try:
    # Load configuration from file
    with open(configFile, "r") as f:
        config = f.read()
except FileNotFoundError:
    print("ERROR: Could not load configuation file")
    sys.exit(1)

config = json.loads(config)  # Convert JSON string into dictionary

image = ImageTools(config)  # Prepare the image tools
image.load()                # Load the image
cells = image.makeCells()   # Make cells out of the image

# Generate the head of the model
head = ConvertTools.createHead(image.getWidth(), image.getLength(), config["model"])

# If the model is 3D, extend the walls and add a floor and ceiling
if (config["model"]["height"] > 1):
    cells = ConvertTools.getExtendedCells(config["model"], cells)
    cells = ConvertTools.addFloorCeiling(image.getWidth(), image.getLength(), config["model"]["height"], cells)

model = ConvertTools.createStructure(head, cells)  # Combine the head and the cells

# Export the JSON string
GeneralTools.export(config["files"]["output"], ConvertTools.getString(model))