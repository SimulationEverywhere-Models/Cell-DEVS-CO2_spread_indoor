# Tools for converting 2D models into 3D models and scaling cells
# Thomas Roller

import sys
import json
from GeneralTools import GeneralTools

# Tools to bring the 2D model into 3D
class ConvertTools:

    # Function: createHead
    # Purpose: create the head of the scenario
    # Arguments:
    #     length: length of the final scenario
    #     width: width of the final scenario
    #     modelConfig: model section of the configuration file
    # Return:
    #     head of the final scenario
    @staticmethod
    def createHead (length, width, modelConfig):
        coords = [length, width]
        if (modelConfig["height"] > 1):
            coords += [modelConfig["height"]]

        return {
            "scenario" : {
                "shape" : coords,
                "wrapped" : False,
                "default_delay": "transport",
                "default_cell_type": "CO2_cell",
                "default_state": {
                    "counter": -1,
                    "concentration": 500,
                    "type": -100,
                    "breathing_counter": 0
                },
                "default_config": {
                    "CO2_cell": {
                        "co2_production": 0.026,
                        "cell_size": 25,
                        "base" : 500,
                        "resp_time" : 1,
                        "window_conc": 400,
                        "vent_conc": 500,
                        "breathing_rate": 5,
                        "time_active": 500,
                        "start_time": 50
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

    # Function: getHeights
    # Purpose: get the heights at which to place each cell type
    # Arguments:
    #     height: height of the final scenario
    #     heights: heights subsection of the model section of the configuration file
    #     cellType: type of cell being checked
    # Return:
    #     list where the first and second elements are the lowest and highest levels where the cellType may appear, respectively
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
    # Function: getExtendedCells
    # Purpose: extend each coordinate in the positive Z direction
    # Arguments:
    #     modelConfig: model section of the configuration file
    #     cells: list containing cells in 2D space
    # Return:
    #     list containing the cells of the extended (3D) scenario
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

    # Function: addFloorCeiling
    # Purpose: add a floor and ceiling (a rectangle of cells which avoids already existing cells)
    # Arguments:
    #     width: width of the final scenario
    #     length: length of the final scenario
    #     height: height of the final scenario
    #     cells: list containing the cells which represent the 3D model
    # Return:
    #     none
    @staticmethod
    def addFloorCeiling (width, length, height, cells, showProgress=False):
        maxStep = width * length

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
                if (not (str([w, l, 0]) in existingCells)):
                    cells.append(GeneralTools.makeCell([w, l, 0], 0, -300, -1))  # floor
                if (not (str([w, l, height - 1]) in existingCells)):
                    cells.append(GeneralTools.makeCell([w, l, height - 1], 0, -300, -1))  # ceiling
        return cells

    # Function: createStructure
    # Purpose: combines the head and the cells
    # Arguments:
    #     head: the head of the scenario (as generated by createHead)
    # Return:
    #     none
    @staticmethod
    def createStructure (head, cells):
        head["cells"] = cells
        return head

    # Function: getString
    # Purpose: get a JSON string representation of a Python dictionary
    # Arguments:
    #     data: Python dictionary
    # Return:
    #     JSON string
    @staticmethod
    def getString (data):
        return json.dumps(data, indent=4)

    # Function: scaleCells
    # Purpose: scale a list of cells (representing 2D space, only)
    # Arguments:
    #     cells: list of cells to be scaled
    #     orgDim: dimensions of original scenario
    #     newDim: dimensions of the desired scenario
    #     debug: whether or not to show debug messages
    #     critMsg: whether or not to show critical messages
    # Return:
    #     list of cells representing a scaled down version of the original scenario
    @staticmethod
    def scaleCells (cells, orgDim, newDim, debug=False, critMsg=False):
        if (orgDim[0] < newDim[0] or orgDim[1] < newDim[1]):
            if (critMsg): print("ERROR: At least one input dimension is smaller than its respective output dimension (cannot extrapolate)")
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

    # Function: getBestCell
    # Purpose: get the cell that best represents the given list of cells
    # Arguments:
    #     cells: list of cells being checked
    # Return:
    #     the cell that best represents the given list of cells
    @staticmethod
    def getBestCell (cells):
        # Prefer SOURCE over WORKSTATIONS over VENTS over DOORS over WINDOWS over WALLS over AIR
        cellTypes = [-200, -700, -600, -400, -500, -300, -100]  # in order of preference
        bestCell = cells[0]
        for cell in cells:
            if (cellTypes.index(cell["state"]["type"]) < cellTypes.index(bestCell["state"]["type"])):
                bestCell = cell
        return bestCell