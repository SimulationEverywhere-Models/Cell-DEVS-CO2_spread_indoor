# Script to convert 2D JSON models into 3D JSON models
# Written by Thomas Roller

import sys
import json
from ImageTools import ImageTools
from ConvertTools import ConvertTools
from GeneralTools import GeneralTools

# Check for proper usage
if (len(sys.argv) != 1 and len(sys.argv) != 2):
    print("Usage: python3 make3D.py [<config file>]")
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

# Get 2D JSON
data = ""
try:
    # Load configuration from file
    with open(config["files"]["input"], "r") as f:
        data = f.read()
except FileNotFoundError:
    print("ERROR: Could not load input file")
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

model = ConvertTools.createStructure(head, cells)  # Combine the head and the cells

# Export the JSON string
GeneralTools.export(config["files"]["output"], ConvertTools.getString(model))