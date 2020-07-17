import json
import sys

symbols = {
    -100 : " ",  # AIR
    -200 : "C",  # CO2_SOURCE
    -300 : "#",  # IMPERMEABLE_STRUCTURE
    -400 : "D",  # DOOR
    -500 : "W",  # WINDOW
    -600 : "V",  # VENT
    -700 : "S"   # WORKSTATION
}

if (len(sys.argv) != 2):
    print("Usage: python3 visualizer.py <input file>")
    sys.exit(0)

config = ""
with open(sys.argv[1], "r") as f:
    config = f.read()

config = json.loads(config)

# Gather relevant information
cells = {}  # key is cell_id, value is type
for cell in config["cells"]:
    cells[str(cell["cell_id"])] = cell["state"]["type"]

is3D = (len(config["scenario"]["shape"]) == 3)

print("""\"{0}\" -> AIR
\"{1}\" -> CO2_SOURCE
\"{2}\" -> IMPERMEABLE_STRUCTURE
\"{3}\" -> DOOR
\"{4}\" -> WINDOW
\"{5}\" -> VENT
\"{6}\" -> WORKSTATION""".format(symbols[-100],
                                 symbols[-200],
                                 symbols[-300],
                                 symbols[-400],
                                 symbols[-500],
                                 symbols[-600],
                                 symbols[-700]))
print()

response = ""
layer = 0
while (response != "q"):
    prompt = ""
    if (is3D):
        prompt = "Show layer (\"q\" to quit): "
        response = input("Show layer (\"q\" to quit): ")
        if (response == "q"):
            continue
    else:
        response = "q"

    if (is3D):
        try:
            layer = int(response)
        except ValueError:
            print("Integer value is required")
            print()
            continue

        if (layer < 0 or layer >= config["scenario"]["shape"][2]):
            print("No information for layer: {0}".format(layer))
            print()
            continue

    result = ""
    for y in range(0, config["scenario"]["shape"][1]):
        for x in range(0, config["scenario"]["shape"][0]):
            coord = [x, y]
            if (is3D):
                coord += [layer]
            if (str(coord) in cells):
                result += symbols[cells[str(coord)]]
            else:
                result += symbols[-100]
            result += " "
        result += "\n"

    print(result)