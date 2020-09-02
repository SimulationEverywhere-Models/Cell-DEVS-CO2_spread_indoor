# Carleton University (ARSLab)
# Thomas Roller

from Parse import Parse
from Graph import Graph
import time
import threading

# Class: Actions
# Purpose: couple functionality from different classes and provide extra output for users/developers
# Arguments:
#     none
class Actions:

    # Class: GraphThread
    # Purpose: thread class used to generate a graph
    # Arguments:
    #     self: enclosing instance (automatic, not user specified)
    #     graphicalElements: dictionary of elements from a GUI which can be modified within the thread
    #     filename: name of the file from which to obtain graphing data (transient mode only)
    #     coords: coordinates for which to generate a graph
    #     cellDict: dictionary of cells read from the file (non-transient mode only)
    class GraphThread(threading.Thread):
        def __init__ (self, graphicalElements, filename="", coords=None, cellDict=None):
            super().__init__(daemon=True)
            self.filename = filename
            self.coords = coords
            self.cellDict = cellDict
            self.graphicalElements = graphicalElements

        # Code to be run in the thread
        def run (self):
            self.graphicalElements["fileButton"]["state"] = "disable"
            self.graphicalElements["graphButton"]["state"] = "disable"
            result = Actions.generateGraph(self.filename, self.coords, self.cellDict)
            if (result[0]):
                self.graphicalElements["statusLabel"].set(f"Showing graph (elapsed: {round(result[1], 2)}s)")
            else:
                self.graphicalElements["statusLabel"].set("No data point matching coordinates found")
            self.graphicalElements["fileButton"]["state"] = "normal"
            self.graphicalElements["graphButton"]["state"] = "normal"

    # Class: LoadThread
    # Purpose: thread class used to load coordinate data (only used in non-transient mode)
    # Arguments:
    #     self: enclosing instance (automatic, not user specified)
    #     graphicalElements: dictionary of elements from a GUI which can be modified within the thread
    #     filename: name of the file from which to obtain coordinate data
    #     coords: coordinates for which to generate a graph
    #     cellDict: dictionary used to store coordinates
    class LoadThread(threading.Thread):
        def __init__ (self, graphicalElements, filename="", cellDict=None):
            super().__init__(daemon=True)
            self.filename = filename
            self.graphicalElements = graphicalElements
            self.cellDict = cellDict

        # Code to be run in the thread
        def run (self):
            self.graphicalElements["fileButton"]["state"] = "disable"
            self.graphicalElements["graphButton"]["state"] = "disable"
            result = Actions.getAllCellStates (self.filename)
            self.cellDict.clear()
            for key in result[0]:
                self.cellDict[key] = result[0][key]
            self.graphicalElements["fileButton"]["state"] = "normal"
            self.graphicalElements["graphButton"]["state"] = "normal"

            self.graphicalElements["statusLabel"].set(f"Storage populated (elapsed: {round(result[1], 2)}s)")
            print("Storage populated")

    # Function: generateGraph
    # Purpose: a wrapper function that generates a graph (displays in a web browser)
    # Arguments:
    #     filename: name of the file from which to obtain graphing data (transient mode only)
    #     coords: coordinates for which to generate a graph
    #     cellDict: dictionary of cells read from the file (non-transient mode only)
    # Return:
    #     list containing the success/failure and the time elapsed
    @staticmethod
    def generateGraph (filename="", coords=None, cellDict=None):
        if (filename == "" and coords is not None and cellDict is not None):
            return Actions.generateGraph_query(cellDict, coords)
        elif (filename != "" and coords is not None and cellDict is None):
            return Actions.generateGraph_transient(filename, coords)
        else:
            print("WARNING: Invalid parameters")
            return [False, 0]

    # Function: generateGraph_transient
    # Purpose: generate a graph directly from a file (displays in a web browser)
    # Arguments:
    #     filename: name of the file from which to obtain graphing data
    #     coords: coordinates for which to generate a graph
    # Return:
    #     list containing the success/failure and the time elapsed
    @staticmethod
    def generateGraph_transient (filename, coords):
        print(f"Parsing file ({filename}) for coords: {coords}")

        startTime = time.monotonic()
        dataPoints = Parse.getCellStates(filename, coords)
        endTime = time.monotonic()

        print(f"Parse complete")

        timeElapsed = endTime - startTime
        print(f"Time taken: {timeElapsed}s")
        print(f"Number of cells: {len(dataPoints)}")

        if (len(dataPoints) == 0):
            print("No data points found (cannot generate graph)")
            return [False, timeElapsed]

        Graph.generateGraph(dataPoints, coords)
        return [True, timeElapsed]

    # Function: generateGraph_query
    # Purpose: generate a graph from a dictionary of coordinates
    # Arguments:
    #     cellDict: dictionary to be used to generate a graph
    #     coords: coordinates for which to generate a graph
    # Return:
    #     list containing the success/failure and the time elapsed
    @staticmethod
    def generateGraph_query (cellDict, coords):
        print(f"Querying dictionary for coords: {coords}")

        coordsString = Parse.getCoordsString(coords)
        if (coordsString not in cellDict):
            print(f"Could not find the provided coordinate in the cell dictionary (length of cellDict: {len(cellDict)})")
            return [False, 0]

        startTime = time.monotonic()
        dataPoints = cellDict[coordsString]
        endTime = time.monotonic()

        timeElapsed = endTime - startTime
        print(f"Time taken: {timeElapsed}s")
        print(f"Number of cells: {len(dataPoints)}")

        if (len(dataPoints) == 0):
            print("No data points found (cannot generate graph)")
            return [False, timeElapsed]

        Graph.generateGraph(dataPoints, coords)
        return [True, timeElapsed]

    # Function: getAllCellStates
    # Purpose: obtain all of the coordinates from a file for every cell
    # Arguments:
    #     filename: name of the file from which to obtain coordinate data
    # Return:
    #     list containing the coordinate data and the time elapsed
    @staticmethod
    def getAllCellStates (filename):
        print(f"Parsing file ({filename})...")
        startTime = time.monotonic()
        states = Parse.getAllCellStates(filename)
        endTime = time.monotonic()
        timeElapsed = endTime - startTime
        print(f"Time taken: {timeElapsed}s")
        return [states, timeElapsed]