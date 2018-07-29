"""
Manger for the differnt calculations needed to provided the requestet data.
See Readme for details.
Can be used directly with a command line tool or with a GUI.

Made by Turidus https://github.com/Turidus/Minecraft-MapMaker
Copyright (c) 2018 Turidus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


"""


import os
import argparse
import re
import itertools

import Parsers
import Saving
import MapColorIDGenerator



def MapMaker(args, outPrioQueue = None):
    """
    Manages the creation of the specified data.
    
    param: args: A struct like class that provides a field for every possible option. For example:
        
                    class Args():
                        
                        pathToImage = None
                        bl = []
                        name = None
                        twoD = False
                        p = True
                        bp = True
                        ba = True
                        s = True
                        minY = 4
                        maxY = 250
                        maxS = 129
                        v = False
                        
          outPrioQueue: A queue.PriorityQueue(). If provided, this will be used as output channel.
                        If None, the output uses print().
                        
    Exception: Raises IOError, VauleError
    """
    
    
    #Managing communication with GUI
    
    prioCounter = itertools.count()
    
    def print2(tulpe): print(tulpe[1])
    
    if outPrioQueue == None:
        
        newPrint = print2
        
    else:
        
        newPrint = outPrioQueue.put
        
    #Settings
    if args.v:
        try:
            with open("version") as vFile:
                newPrint ((prioCounter.__next__(), vFile.read()))
        except IOError:
            newPrint((prioCounter.__next__(), "Version file not found"))

    newPrint((prioCounter.__next__(),"Setting up"))
    
    imagePath = os.path.abspath(args.pathToImage)
    
    if not os.path.isfile(imagePath):
        raise IOError("path does not point at a file")
    
    if args.n == None:
        imageName = os.path.split(os.path.splitext(imagePath)[0])[1]
    else:
        imageName = re.sub(r'[^a-zA-Z0-9_]', '', args.n)
    
    if args.twoD:
        mapColorIDDic = MapColorIDGenerator.mapColorIDGenerator2D(args.bl)
    else:
        mapColorIDDic = MapColorIDGenerator.mapColorIDGenerator3D(args.bl)
        
    
    
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
        newPrint((prioCounter.__next__(),"Your schematic size is bigger 129. be careful when importing such large schematics"))
    
    

    newPrint((prioCounter.__next__(),"Finished setting up"))

    
    #Calculating intermediaries


    newPrint((prioCounter.__next__(),"Calculating rgbMatrix"))  
    rgbMatrix = Parsers.imageFileToRGBMatrix(imagePath)
    newPrint((prioCounter.__next__(),"Done"))

    
    newPrint((prioCounter.__next__(),"Calculating mapColorIDMatrix"))
    mapColorIDMatrix = Parsers.rgbMatrixTomapColorID(rgbMatrix,mapColorIDDic)
    newPrint((prioCounter.__next__(),"Done"))

    
    if args.bp or args.s:
        newPrint((prioCounter.__next__(),"Calculating positionMatrix"))
        positionMatrix = Parsers.mapColorIDToPositionMatrix(mapColorIDMatrix, positionMatrixMinY, positionMatrixMaxY)
        newPrint((prioCounter.__next__(),"Done"))

        
    if args.s:
        newPrint((prioCounter.__next__(), "Calculating Schematic"))
        tag_Compound_List = Parsers.positionMatrixToTag_CompoundList(positionMatrix, mapColorIDDic, positionMatrixMinY, positionMatrixMaxY, maxSchematicSize)
        newPrint((prioCounter.__next__(),"Done"))
    
    #Calculating and saving results
    

    if args.ba:
        newPrint((prioCounter.__next__(),"Saving AmountTXT"))
        Saving.saveAmountTxT(mapColorIDMatrix,mapColorIDDic,imageName)

    
    if args.bp:
        newPrint((prioCounter.__next__(),"Saving PositionTXT"))
        Saving.saveBlockPositionTxT(positionMatrix,mapColorIDDic, imageName)
    
    if args.p:
        newPrint((prioCounter.__next__(),"Saving Image"))
        Saving.saveImage(mapColorIDMatrix, mapColorIDDic, imageName)
        
    if args.s:
        newPrint((prioCounter.__next__(),"Saving Schematic"))
        Saving.saveSchematic(tag_Compound_List, imageName)
        
    newPrint((prioCounter.__next__(),"Finished with this image"))



if __name__ == "__main__":
    cmdparser = argparse.ArgumentParser(description="This procesess image files into multiple files\nthat help to build minecraft ingame maps.")
    cmdparser.add_argument("pathToImage", help="The path to the image that should be processed\n")
    cmdparser.add_argument("-bl", nargs="+", help="Optional list of BaseColorIDs that should not be used\n")
    cmdparser.add_argument("-n", help = "Optional name for the resulting files\n")
    cmdparser.add_argument("-v", action="store_true", help =" Show version")
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
