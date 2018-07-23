import Parsers
import Saving
import MapIDGenerator
import pickle
import os
import argparse
import re
import queue



def MapMaker(args, outPrioQueue = None):
    #Managing communication with GUI
    
    class Prio():
        prio: int = -1
        
        def add_get(self):
            
            self.prio += 1
            
            return self.prio
    
    def print2(tulpe):
        
        print(tulpe[1])
    
    priority = Prio()
    
    if outPrioQueue == None:
        
        newPrint = print2
        
    else:
        
        newPrint = outPrioQueue.put
        
    #Settings

    newPrint((priority.add_get(),"Setting up"))
    
    imagePath = os.path.abspath(args.pathToImage)
    
    if not os.path.isfile(imagePath):
        raise IOError("path does not point at a file")
    
    if args.n == None:
        imageName = os.path.split(os.path.splitext(imagePath)[0])[1]
    else:
        imageName = re.sub(r'[^a-zA-Z0-9_]', '', args.n)
    
    if args.twoD:
        mapIDDic = MapIDGenerator.mapIDGenerator2D(args.bl)
    else:
        mapIDDic = MapIDGenerator.mapIDGenerator3D(args.bl)
    
    
    positionMatrixMinY = int(args.minY) if args.minY else 4
    
    positionMatrixMaxY = int(args.maxY) if args.maxY else 250
    
    if 0 > positionMatrixMinY or positionMatrixMinY > 251:
        raise ValueError("minY is smaller 0 or bigger 251")
    
    if 4 > positionMatrixMaxY or positionMatrixMaxY > 255:
        raise ValueError("maxY is smaller 4 or bigger 255")
    
    if positionMatrixMinY >= positionMatrixMaxY - 3:
        raise ValueError("minY and maxY are to close toadd_gether (closer than 4) or minY is bigger than maxY")
        
    maxSchematicSize = int(args.maxS) if args.maxS else 129
    
    if maxSchematicSize < 1:
        raise ValueError("maxS is smaller than 1")
    elif maxSchematicSize > 129:
        newPrint((priority.add_get(),"Your schematic size is bigger 129. be careful when importing such large schematics"))
    
    

    newPrint((priority.add_get(),"Finished setting up"))

    
    #Calculating intermediaries


    newPrint((priority.add_get(),"Calculating rgbMatrix"))
        
    rgbMatrix = Parsers.imageFileToRGBMatrix(imagePath)
    
    

    newPrint((priority.add_get(),"Done"))

    
    newPrint((priority.add_get(),"Calculating mapIDMatrix"))
    mapIDMatrix = Parsers.rgbMatrixToMapID(rgbMatrix,mapIDDic)
    

    newPrint((priority.add_get(),"Done"))

    
    if args.bp or args.s:
        newPrint((priority.add_get(),"Calculating positionMatrix"))
        positionMatrix = Parsers.mapIDToPositionMatrix(mapIDMatrix, positionMatrixMinY, positionMatrixMaxY)
    

    newPrint((priority.add_get(),"Done"))

        
    if args.s:
        newPrint((priority.add_get(), "Calculating Schematic"))
        tag_Compound_List = Parsers.positionMatrixToTag_CompoundList(positionMatrix, mapIDDic, positionMatrixMinY, positionMatrixMaxY, maxSchematicSize)
        newPrint((priority.add_get(),"Done"))
    
    #Calculating and saving results
    

    if args.ba:
        newPrint((priority.add_get(),"Saving AmountTXT"))
        Saving.saveAmountTxT(mapIDMatrix,mapIDDic,imageName)

    
    if args.bp:
        newPrint((priority.add_get(),"Saving PositionTXT"))
        Saving.saveBlockPositionTxT(positionMatrix,mapIDDic, imageName)
    
    if args.p:
        newPrint((priority.add_get(),"Saving Image"))
        Saving.saveImage(mapIDMatrix, mapIDDic, imageName)
        
    if args.s:
        newPrint((priority.add_get(),"Saving Schematic"))
        Saving.saveSchematic(tag_Compound_List, imageName)
        
    newPrint((priority.add_get(),"Finished with this image"))

if __name__ == "__main__":
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
    MapMaker(args)
