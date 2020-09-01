# Carleton University (ARSLab)
# Thomas Roller

# This program can be used to generate graphs which plot the concentration of CO2 for a specific
# set of coordinates over time. The program uses output files from the Cadmium simulator to
# generate the graphs. (The program has been tested using the "output_messages.txt" file primarily
# but should also function without issue using the "state.txt" output file.)
#
# There are two mode for the program: transient and store.
#
# === Transient Mode ===
# Transient mode causes the program to consult the output file each time a new graph is requested.
# This process results in quicker initial loading times and a smaller memory footprint (especially
# for larger output files) but requires more time to generate the graph as the entire file must
# be parsed each time.
#
# == Store Mode ===
# Store mode causes the program to load the entire output file into memory. There are no checks
# to ensure that the file will fit into memory and the program may crash for exceedingly large
# files. This mode also results in significant initial loading times. However, once the file is
# loaded, subsequent requests for graphs will be very quick as the program only needs to do a
# quick dictionary search.

from Interface import Interface
import sys
import argparse

argParser = argparse.ArgumentParser(description="Create graphs which plot CO2 concentration over time",
                                    allow_abbrev=False)

argParser.add_argument("--filename",
                        "-f",
                        type=str,
                        action="store",
                        help="name of file to be loaded",
                        dest="filename")

argParser.add_argument("--store",
                       "-s",
                       action="store_true",
                       help="turn on store mode (as opposed to the default of transient mode)",
                       dest="store")

args = argParser.parse_args()

transient = not args.store

mode = "transient" if transient else "store"
print(f"Mode: {mode}")

if (args.filename is None):
    Interface.start(transient=transient)
else:
    Interface.start(filename=args.filename, transient=transient)