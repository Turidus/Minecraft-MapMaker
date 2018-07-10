import Parsers
import Saving
import MapIDGenerator
import pickle
import os
import argparse


cmdparser = argparse.ArgumentParser(description="This procesess image files into multiple files\nthat help to build minecraft ingame maps.")
cmdparser.add_argument("pathToImage", help="The path to the image that should be processed")
cmdparser.add_argument("-bl", nargs="+", help="Optional list of BaseColorIDs that should not be used")
cmdparser.add_argument("-n", help = "Optional name for the resulting files")
cmdparser.add_argument("-twoD", action="store_true", help = "If added, this will generate a flat map instead of a stepped one")
cmdparser.add_argument("-P", action="store_true", help = "If added, this will generated a preview picture of the map")


args = cmdparser.parse_args()

#Settings
imagePath = os.path.abspath(args.pathToImage)

if not os.path.isfile(imagePath):
    raise IOError("path does not point at a file")

if args.n == None:
    imageName = os.path.split(os.path.splitext(imagePath)[0])[1]
else:
    imageName = args.n

if args.twoD:
    mapIDList = MapIDGenerator.mapIDGenerator2D(args.bl)
else:
    mapIDList = MapIDGenerator.mapIDGenerator3D(args.bl)


#Calculating intermediaries 
rgbMatrix = Parsers.imageFileToRGBMatrix(imagePath)

mapIDMatrix = Parsers.rgbMatrixToMapID(rgbMatrix,mapIDList)

positionMatrix = Parsers.mapIDToPositionMatrix(mapIDMatrix, mapIDList)

#Calculating and saving results

Saving.saveAmountTxT(mapIDMatrix,mapIDList,imageName)
Saving.saveBlockPositionTxT(positionMatrix,mapIDList, imageName)

if args.P:
    Saving.saveImage(mapIDMatrix, mapIDList, imageName)
