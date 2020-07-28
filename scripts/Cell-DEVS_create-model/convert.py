# Script to convert image files into models (2D and 3D)
# Thomas Roller

import argparse
import sys
from Control import Control
from ImageTools import ImageTools

# Check for proper usage
#if (len(sys.argv) > 3):
#    print("Usage: python3 convertImage.py [<config file>] [<extrapolate: true/false>]")
#    sys.exit(0)

import argparse

argParser = argparse.ArgumentParser(description="Convert images and 2D models into their 2D or 3D counterparts",
                                    allow_abbrev=False)

argParser.add_argument("--config",
                       "-c",
                       type=str,
                       action="store",
                       help="path to configuration file",
                       dest="config")

argParser.add_argument("--dimensions",
                       "-d",
                       type=int,
                       action="store",
                       nargs=2,
                       help="dimensions of the output scenario (format: HOR VERT)",
                       dest="dim")

argParser.add_argument("--no-debug",
                       action="store_true",
                       help="turn off debugging/information messages",
                       dest="no_debug")

args = argParser.parse_args()

try:
    Control.start(args)
except KeyboardInterrupt:
    print("Caught interrupt -- aborting")