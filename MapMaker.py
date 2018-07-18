import Parsers
import Saving
import MapIDGenerator
import pickle
import os
import argparse


cmdparser = argparse.ArgumentParser(description="This procesess image files into multiple files\nthat help to build minecraft ingame maps.")
cmdparser.add_argument("pathToImage", help="The path to the image that should be processed\n")
cmdparser.add_argument("-bl", nargs="+", help="Optional list of BaseColorIDs that should not be used\n")
cmdparser.add_argument("-n", help = "Optional name for the resulting files\n")
cmdparser.add_argument("-twoD", action="store_true", help = "If added, this will generate a flat map instead of a stepped one\n")
cmdparser.add_argument("-p", action="store_false", help = "If added, this will prevent the generation of a preview picture of the map\n")
cmdparser.add_argument("-bp", action="store_false", help = "If added, this will prevent the generation of a list of the block positions\n")
cmdparser.add_argument("-ba", action="store_false", help = "If added, this will prevent the generation of a list of needed amounts of blocks\n")
cmdparser.add_argument("-s", action="store_false", help = "If added, this will prevent the generation of the schematic file\n")
cmdparser.add_argument("-minY", help = "Defines the minimum Y coordinate at which blocks are placed.\n Default = 4. Should be the block you will be standing on for schematics\n")
cmdparser.add_argument("-maxY", help = "Defines the maximum Y coordinate at which blocks are placed. Default = 250. Does not impact schematics\n")
cmdparser.add_argument("-maxS", help = "Defines the maximum sizie in X and Z of a schematic.\n Default = 128. If the picture is bigger, multiple schematics will be generated")


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


positionMatrixMinY = int(args.minY) if args.minY else 4

positionMatrixMaxY = int(args.maxY) if args.maxY else 250

if positionMatrixMinY >= positionMatrixMaxY - 3:
    raise ValueError("minY and maxY are to close together (closer than 4) or minY is bigger than maxY")
    
maxSchematicSize = int(args.maxS) if args.maxS else 129



#Calculating intermediaries 
rgbMatrix = Parsers.imageFileToRGBMatrix(imagePath)

mapIDMatrix = Parsers.rgbMatrixToMapID(rgbMatrix,mapIDList)

if args.bp or args.s:
    positionMatrix = Parsers.mapIDToPositionMatrix(mapIDMatrix, mapIDList, positionMatrixMinY, positionMatrixMaxY)

if args.s:
    tag_Compound = Parsers.positionMatrixToTag_CompoundList(positionMatrix, mapIDList, positionMatrixMinY, positionMatrixMaxY, maxSchematicSize)


#Calculating and saving results

if args.ba:
    Saving.saveAmountTxT(mapIDMatrix,mapIDList,imageName)

if args.bp:
    Saving.saveBlockPositionTxT(positionMatrix,mapIDList, imageName)

if args.p:
    Saving.saveImage(mapIDMatrix, mapIDList, imageName)
    
if args.s:
    Saving.saveSchematic(tag_Compound, imageName)


