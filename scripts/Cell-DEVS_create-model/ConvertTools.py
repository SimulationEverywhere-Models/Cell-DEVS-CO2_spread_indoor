# Tools for converting 2D models into 3D models and scaling cells
# Thomas Roller

import sys
import json
from GeneralTools import GeneralTools

# Tools to bring the 2D model into 3D
class ConvertTools:

    # Create the head of the JSON file
    @staticmethod
    def createHead (length, width, modelConfig):
        coords = [length, width]
        if (modelConfig["height"] > 1):
            coords += [modelConfig["height"]]

        data = {
            "scenario" : {
                "shape" : coords,
                "wrapped" : False,
                "default_delay" : "transport",
                "default_cell_type" : "CO2_cell",
                "default_state" : {
                    "counter": -1,
                    "concentration" : 500,
                    "type" : -100
                },
            "default_config" : {
                    "CO2_cell" : {
                        "conc_increase" : 143.2,
                        "base" : 500,
                        "resp_time" : 5,
                        "window_conc" : 400,
                        "vent_conc" : 300
                    }
                },
                "neighborhood": [
                    {
                        "type" : modelConfig["neighbourhood"],
                        "range" : modelConfig["range"]
                    }
                ]
            },
            "cells" : []
        }
        return data

    # Get the heights at which to place each cell type
    # Returns a list where the first element is the lowest cell it may appear in and
    # the second element is one above the highest cell it may appear in
    @staticmethod
    def getHeights (height, heights, cellType):
        # WALL
        if (cellType == -300):
            return [1, height - 2]  # keep in mind that HEIGHT is dirived from the shape
        
        # DOOR
        elif (cellType == -400):
            return [1, heights["door_top"]]

        # WINDOW
        elif (cellType == -500):
            return [heights["window"]["bottom"], heights["window"]["top"]]

        # VENTILATION
        elif (cellType == -600):
            return [heights["vent"], heights["vent"]]

        # WORKSTATION or CO2_SOURCE
        elif (cellType == -700 or cellType == -200):
            return [heights["workstation"], heights["workstation"]]

        # Otherwise
        else:
            return [0, 0]  # for loop does no iterations

    # Extent each coordinate in the positive Z direction
    # This brings the 2D model into 3D space
    @staticmethod
    def getExtendedCells (modelConfig, cells):
        allCells = []
        for cell in cells:
            # Add given cells at appropriate heights
            if (modelConfig["walls_only"] and cell["state"]["type"] != -300):
                continue

            heights = ConvertTools.getHeights(modelConfig["height"], modelConfig["heights"], cell["state"]["type"])

            # Go through all Z values (floor and ceiling included)
            for z in range(0, modelConfig["height"]):
                # If Z value is within cell's permitted values, add wall cell at that coordinate
                if (z in range(heights[0], heights[1] + 1)):
                    allCells.append(GeneralTools.makeCell(
                        cell["cell_id"] + [z],
                        cell["state"]["concentration"],
                        cell["state"]["type"],
                        cell["state"]["counter"]
                    ))
                # If Z value is not within cell's permitted values AND that cell requires walls
                # above/below (DOOR and WINDOW), add wall cell at that coordinate
                elif (cell["state"]["type"] == -400 or cell["state"]["type"] == -500):
                    allCells.append(GeneralTools.makeCell(
                        cell["cell_id"] + [z],
                        0,
                        -300,
                        -1
                    ))
        return allCells

    # Add a floor and ceiling
    # This is fairly simple as it just fills in the entire
    # length by width rectangle at the floor and ceiling levels
    @staticmethod
    def addFloorCeiling (width, length, height, cells, showProgress=False):
        maxStep = width * length
        newCells = []

        # Add cells that are on the level of the floor and ceiling to a set to improve membership lookup time
        existingCells = set()
        for cell in cells:
            if (cell["cell_id"][2] == 0 or cell["cell_id"][2] == height - 1):
                existingCells.add(str(cell["cell_id"]))

        for w in range (0, width):
            for l in range (0, length):
                if (showProgress):
                    currStep = ((w + 1) * length) + (l + 1)
                    GeneralTools.printProgress(currStep, maxStep)
                if (not( str([w, l, 0]) in existingCells)):
                    newCells.append(GeneralTools.makeCell([w, l, 0], 0, -300, -1))  # floor
                if (not( str([w, l, height - 1]) in existingCells)):
                    newCells.append(GeneralTools.makeCell([w, l, height - 1], 0, -300, -1))  # ceiling
        return cells + newCells

    # Combines the head and the cells
    @staticmethod
    def createStructure (head, cells):
        head["cells"] = cells
        return head

    # Returns a JSON string representation of the dictionary
    @staticmethod
    def getString (data):
        return json.dumps(data, indent=4)

    # Scale a list of cells
    @staticmethod
    def scaleCells (cells, orgDim, newDim, debug=False):
        if (orgDim[0] < newDim[0] or orgDim[1] < newDim[1]):
            if (debug): print("| ERROR: At least one input dimension is smaller than its respective output dimension (cannot extrapolate)")
            sys.exit(1)

        newCells = []
        groups = {}

        scaleX = float(newDim[0] - 1) / float(orgDim[0])
        scaleY = float(newDim[1] - 1) / float(orgDim[1])
        if (debug):
            print(f"| Image dimensions: {orgDim}")
            print(f"| Final dimensions: {newDim}")
            print(f"| Approximate X scale factor: {round(scaleX * 100)}%")
            print(f"| Approximate Y scale factor: {round(scaleY * 100)}%")

        for cell in cells:
            # Scale the cell_id of each cell
            cell["cell_id"][0] = round(cell["cell_id"][0] * scaleX)
            cell["cell_id"][1] = round(cell["cell_id"][1] * scaleY)

            # Group cells with the same cell_id into a dictionary
            currX = cell["cell_id"][0]
            currY = cell["cell_id"][1]
            if (f"{currX},{currY}" in groups):
                groups[f"{currX},{currY}"].append(cell)
            else:
                groups[f"{currX},{currY}"] = [cell]

        # Get the most representative cell from each group
        for key in groups:
            newCells.append(ConvertTools.getBestCell(groups[key]))
        
        return newCells

    # Get the cell that best represents the given list
    @staticmethod
    def getBestCell (cells):
        # Prefer SOURCE over WORKSTATIONS over VENTS over DOORS over WINDOWS over WALLS over AIR
        cellTypes = [-200, -700, -600, -400, -500, -300, -100]  # in order of preference
        bestCell = cells[0]
        for cell in cells:
            if (cellTypes.index(cell["state"]["type"]) < cellTypes.index(bestCell["state"]["type"])):
                bestCell = cell
        return bestCell