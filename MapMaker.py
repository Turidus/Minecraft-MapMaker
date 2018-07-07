import Parsers
import Saving
import MapIdGenerator
import pickle
import os
import argparse


cmdparser = argparse.ArgumentParser(description="This procesess image files into multiple files\nthat help to build minecraft ingame maps.")
cmdparser.add_argument("pathToImage", help="The path to the image that should be processed")
cmdparser.add_argument("-bl", nargs="+", help="Optional list of BaseColorIDs that should not be used")

args = cmdparser.parse_args()

imagePath = os.path.abspath(args.pathToImage)
if not os.path.isfile(imagePath):
    raise IOError("path does not point at a file")

imageName = os.path.split(os.path.splitext(imagePath)[0])[1]

mapIDList = MapIdGenerator.mapIDGenerator(args.bl)

rgbMatrix = Parsers.imageFileToRGBMatrix(imagePath)
mapIDMatrix = Parsers.rgbMatrixToMapID(rgbMatrix,mapIDList)

Saving.saveAmountTxT(mapIDMatrix,mapIDList,imageName)
Saving.saveBlockPositionTxT(mapIDMatrix, mapIDList, imageName)

