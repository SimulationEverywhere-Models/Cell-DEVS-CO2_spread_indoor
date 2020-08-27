# Carleton University (ARSLab)
# Thomas Roller

from DataPoint import DataPoint

# Class: Parse
# Purpose: provide file I/O and parsing capabilities
# Arguments:
#     none
class Parse:

    # Function: getCellStates
    # Purpose: get data on a coordinate by consulting the file for each query
    # Arguments:
    #     filename: name of file to search
    #     coords: coordinates for which to get information
    # Return:
    #     list of DataPoint objects
    @staticmethod
    def getCellStates (filename, coords):
        dataPoints = []
        currTime = 0
        with open(filename, "r") as f:
            for line in f:
                # Update time
                if (Parse.isTime(line)):
                    # If there is no cell with the given coordinates in a particular time, use the previous
                    if (currTime > 0 and len(dataPoints) > 0 and dataPoints[-1].getTime() != currTime):
                        dataPoints.append(DataPoint(currTime, dataPoints[-1].getConcentration()))
                    currTime = int(line)
                    continue

                # Adds cell to list
                if (Parse.matchesCoords(line, coords)):
                    dataPoint = Parse.getDataPoint(currTime, line)
                    if (dataPoint not in dataPoints):
                        dataPoints.append(dataPoint)
        return dataPoints

    # Function: getAllCellStates
    # Purpose: get data on all coordinates present in the file
    # Arguments:
    #     filename: name of file to parse
    # Return:
    #     dictionary containing data on coordinates
    @staticmethod
    def getAllCellStates (filename):
        dataPoints = {}
        currTime = 0
        currCoords = ""
        with open(filename, "r") as f:
            for line in f:
                # Update time
                if (Parse.isTime(line)):
                    currTime = int(line)
                    continue

                currCoords = Parse.getCoordsString(Parse.getCoords(line))
                dataPoint = Parse.getDataPoint(currTime, line)
                if (currCoords not in dataPoints):
                    dataPoints[currCoords] = [dataPoint]
                elif (dataPoint not in dataPoints[currCoords]):
                    dataPoints[currCoords].append(dataPoint)

        print("Cleaning data points...")
        return Parse.cleanDataPoints(filename, dataPoints, currTime)

    # Function: cleanDataPoints
    # Purpose: adds missing DataPoint objects that could not parsed from a file
    # Arguments:
    #     filename: name of file from which the DataPoint objects were parsed
    #     dataPoints: dictionary of dataPoints before being cleaned
    # Return:
    #     dictionary containing complete set of DataPoints
    @staticmethod
    def cleanDataPoints (filename, dataPoints, numSteps):
        for key in dataPoints:
            for i in range(0, numSteps):
                if (i < len(dataPoints[key])):
                    if (dataPoints[key][i].getTime() != i):
                        dataPoints[key].insert(i, DataPoint(i, dataPoints[key][i - 1].getConcentration()))
                else:
                    dataPoints[key].append(DataPoint(i, dataPoints[key][-1].getConcentration()))
        return dataPoints

    # Function: matchCoords
    # Purpose: determine whether a line contains information about a set of  coordinates
    # Arguments:
    #     line: string being checked
    #     coords: coordinates being used as search criterion
    # Return:
    #     whether or not the line contains information about a set of coordinates
    @staticmethod
    def matchesCoords (line, coords):
        return coords == Parse.getCoords(line)

    # Function: getCoords
    # Purpose: get a set of coordinates from a string
    # Arguments:
    #     line: line to be parsed
    # Return:
    #     list containing a set of coordinates
    @staticmethod
    def getCoords (line):
        return [int(element) for element in line[line.find("(") + 1:line.find(")")].split(",")]

    # Function: getCoordsString
    # Purpose: convert a list of coordinates into a string
    # Arguments:
    #     coords: coordinates to be converted
    # Return:
    #     string representing a set of coordinates
    @staticmethod
    def getCoordsString (coords):
        result = ""
        for coord in enumerate(coords):
            result += str(coord[1])
            if (coord[0] != len(coords) - 1):
                result += ","
        return result

    # Function: getDataPoint
    # Purpose: create a DataPoint
    # Arguments:
    #     time: time being used to create a DataPoint
    #     line: string which contains information about the concentration for a specific time-step
    # Return:
    #     DataPoint instance that represents the concentration at a specific time-step for a set of coordinates
    @staticmethod
    def getDataPoint (time, line):
        return DataPoint(time, [int(element) for element in line[line.rfind("<") + 1:line.rfind(">")].split(",")][1])

    # Function: isTime
    # Purpose: determine if a line represents a time-step indicator
    # Arguments:
    #     line: line being checked
    # Return:
    #     whether or not a line represents a time-step indicator
    @staticmethod
    def isTime (line):
        try:
            int(line)
            return True
        except:
            return False