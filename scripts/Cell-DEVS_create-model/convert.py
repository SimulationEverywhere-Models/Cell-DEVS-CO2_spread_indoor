# Script to convert image files into models (2D and 3D)
# Thomas Roller

import argparse
import sys
from Control import Control
from ImageTools import ImageTools

import argparse

argParser = argparse.ArgumentParser(description="Convert images and 2D models into their 2D or 3D counterparts",
                                    allow_abbrev=False)

argParser.add_argument("config",
                       type=str,
                       action="store",
                       help="path to configuration file")

argParser.add_argument("--dimensions",
                       "-d",
                       type=int,
                       action="store",
                       nargs=2,
                       help="dimensions of the output scenario (format: HOR VERT)",
                       metavar="int",
                       dest="dim")

argParser.add_argument("--progress-msg",
                       "-p",
                       action="store_true",
                       help="turn on progress messages (off by default)",
                       dest="prog_msg")

argParser.add_argument("--img-msg",
                       "-i",
                       action="store_true",
                       help="turn on image parsing error/information messages (off by default)",
                       dest="img_msg")

argParser.add_argument("--no-crit-msg",
                       "-c",
                       action="store_true",
                       help="turn off critical messages (on by default)",
                       dest="no_crit_msg")

args = argParser.parse_args()

try:
    Control.start(args)
except KeyboardInterrupt:
    if (not args.no_crit_msg): print("Caught interrupt")