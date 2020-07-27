# Script to convert image files into models (2D and 3D)
# Written by Thomas Roller

import sys
from Control import Control

# Check for proper usage
if (len(sys.argv) != 1 and len(sys.argv) != 2):
    print("Usage: python3 convertImage.py [<config file>]")
    sys.exit(0)

Control.start(sys.argv)