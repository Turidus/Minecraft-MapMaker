from math import sqrt
from PIL import Image
import io
import sys
import copy
import random as rnd
import nbt

def _rgbDistance(rgbFromPixel,rgbFromList):
    
    rDif = rgbFromPixel[0] - rgbFromList[0]
    gDif = rgbFromPixel[1] - rgbFromList[1]
    bDif = rgbFromPixel[2] - rgbFromList[2]
    
    return sqrt( rDif ** 2 + gDif ** 2 + bDif ** 2)
    
def _blockFinder(mapID,mapIdList):
    
    for entry in mapIdList:
        
        if entry[0] == mapID:
            return entry[2:]
            
def _openImage(pathString):
    
    try:
        with open(pathString,"rb") as file: 
            img = Image.open(io.BytesIO(file.read()))
    
    except(IOError):
        raise IOError("File is not a (supported) image")
    
    return img
    
def _addOneToAllY(positionMatrix):
    for z in range(len(positionMatrix)):
        for x in range(len(positionMatrix[z])):
            positionMatrix[z][x][3] += 1
            
def _sortkeyForUsedBlocks(string):
    
    if "_" not in string:        
        return (int(string), -1)
    else:
        splitString = string.split("_")
        return (int(splitString[0]),int(splitString[1]))
    
def imageFileToRGBMatrix(pathString):
    
    img = _openImage(pathString)

    if img.size[0] == 0 or img.size[1] == 0:
        raise IOError("Inpit image was empty")
        
    if img.mode != "RGB":
        
        img = img.convert("RGB")
    
    
    rgbMatrix  = []
    
    for y in range(img.height):
        
        tempLine = []
        
        for x in range(img.width):
            
            tempLine.append(img.getpixel((x,y)))
        
        rgbMatrix.append(tempLine)
        
    return rgbMatrix
    
def rgbMatrixToMapID(rgbMatrix, mapIdList):
    
    mapIdMatrix = []
    curRGB = (-1,-1,-1)
    curMapID = "0"

    for y in range(len(rgbMatrix)):
        
        tempLine = []
        
        for x in range(len(rgbMatrix[y])):
            
            if curRGB == rgbMatrix[y][x]:       #Pictures often have groups of pixels with the same value
                tempLine.append(curMapID)       #This saves a loop through the MapIdList in that case
                continue
            else:
                curRGB = rgbMatrix[y][x]
            
            curDif = 450
            
            for entry in mapIdList:
                
                tempDif = _rgbDistance(rgbMatrix[y][x],entry[1])

                if tempDif < curDif:
                    
                    curDif = tempDif
                    curMapID = entry[0]
                
            tempLine.append(curMapID)
        
        mapIdMatrix.append(tempLine)

    return mapIdMatrix

def mapIDToAmountString(mapIDMatrix,mapIdList):
    
    usedBlocks = {}
    
    for y in range(len(mapIDMatrix)):
        
        
        
        for x in range(len(mapIDMatrix[y])):
            
            block = _blockFinder(mapIDMatrix[y][x],mapIdList)
            
            if block[1] not in usedBlocks:
                
                usedBlocks[block[1]] = [1,block[0]]
            
            else:
                usedBlocks[block[1]][0] += 1
    
    retString = "You need follwing amount of blocks\n"
    retString += "{:^40}{:^10}{:^10}\n".format("Blockname","BlockID","Amount")
    
    usedBlockKeys = list(usedBlocks.keys())
    usedBlockKeys.sort(key = _sortkeyForUsedBlocks)
    
    for key in usedBlockKeys:
        
        if "_" in key:
            blockID =  key.replace("_",":")
        
        else:
            blockID =  key
            
        retString += "{:^40}{:^10}{:>10}\n".format(usedBlocks[key][1], blockID, str(usedBlocks[key][0]))
    
    return retString
    
def mapIDToPositionMatrix(mapIDMatrix,mapIDList,minimumY = 6,maximumY = 250):
    
    positionMatrix = []
    startY = int((maximumY - minimumY) / 2)
    
    
    height = len(mapIDMatrix) + 1 #+ 1 because there will be an additional line added to the matrix
    width = len(mapIDMatrix[0])
    
    workMatrix = copy.deepcopy(mapIDMatrix)
    
    zeroLine = [] #This adds a additinal row of blocks into the map, to shade the first row of the image on the map correctly
                    
    
    for zeroPosition in range(width):
        zeroLine.append(44)
    workMatrix.insert(0,zeroLine)
    
    
    for z in range(height):
        
        tempLine = []
        needsToBeRaised = False
        
        for x in range(width):
            
            if z == 0:
                tempLine.append([44,x,height,startY])
            
            else:
                if int(workMatrix[z][x]) % 4 == 1:
                    posY = positionMatrix[z-1][x][3]     
                                  
                elif int(workMatrix[z][x]) % 4 == 2:
                    
                    posY = positionMatrix[z-1][x][3] + 1
                
                else:

                    if not needsToBeRaised and positionMatrix[z-1][x][3] <= minimumY:
                    #This prevents block from being placed under the minimum Y position 
                    #0-5 are the bedrock level on survivale Maps

                        #_addOneToAllY(positionMatrix)
                        #for item in tempLine:
                        #    item[3] += 1
                        needsToBeRaised = True
                    posY = positionMatrix[z-1][x][3] - 1
                
                
                tempLine.append([workMatrix[z][x],x, height - (z + 1), posY])
                
                
        positionMatrix.append(tempLine)
        if needsToBeRaised:
            _addOneToAllY(positionMatrix)
    
    #This breaks long runs that occure in big pictures and
    #exeeds the height limit of 255 blocks on a minecraft map (or any given maximum Y position)
    #It also leads to a mismatched color pixel on the map.
    #To prevent this from lines in pictures with areas of similar colors, this is spread over a range of blocks
    for x in range(len(positionMatrix[0])):
        
        for z in range(len(positionMatrix)):
            
            if positionMatrix[z][x][3] >= maximumY:

                zOffset = rnd.randint(0,min(10,z))

                for deltaZ in range(0,len(positionMatrix) - (z - zOffset)):

                    positionMatrix[z - zOffset + deltaZ][x][3] = minimumY + deltaZ
            
    
    return positionMatrix

    

    
def positionMatrixToPositionString(positionMatrix,mapIDList):
    
    curMapID = 44
    curBlock = "Cobbelstone"
    retString = "{:^40}({:^5},{:^5},{:^5})\n".format("Block","X","Z","Y")
    
    for x in range(len(positionMatrix[0])):
        for z in range(len(positionMatrix)):
            if positionMatrix[z][x][0] != curMapID:
                curMapID = positionMatrix[z][x][0]
                curBlock = _blockFinder(curMapID,mapIDList)[0]
                
            retString += "{:^40}({:^5},{:^5},{:^5})\n".format(curBlock,positionMatrix[z][x][1], positionMatrix[z][x][2],positionMatrix[z][x][3])
    
    return retString



def mapIDToPicture(mapIDMatrix, mapIDList):
    
    curMapID = 0
    curRGB = (0,0,0)
    
    image = Image.new("RGB", (len(mapIDMatrix[0]),len(mapIDMatrix)))
    
    for y in range(len(mapIDMatrix)):
        
        for x in range(len(mapIDMatrix[0])):
            
            if curMapID != mapIDMatrix[y][x]:
                
                for item in mapIDList:
                    
                    if item[0] == mapIDMatrix[y][x]:
                        
                        curRGB = item[1]
                        break
            
            image.putpixel((x,y),curRGB)
            
    return image
    


def positionMatrixToTag_Compound(positionMatrix, mapIDList, minY, maxY):
    
    maxSchematicHeight = maxY - minY
    lowestUsedY = maxY
    highestUsedY = minY
    length = len(positionMatrix)
    width = len(positionMatrix[0])
    curMapID = 0
    curBlockID = 0
    
    blockList = []
    blockDataList = []
    
    schematicCubix = [ [["0" for i in range(width)] for i in range(length)] for i in range(maxSchematicHeight)]
    
    for z in range(length):
        
        for x in range(width):
            
            if positionMatrix[z][x][0] != curMapID:
                curMapID = positionMatrix[z][x][0]
                curBlockID = _blockFinder(curMapID,mapIDList)[1]


            
            correctedY = positionMatrix[z][x][3] - minY
            schematicCubix[correctedY][z][x] = curBlockID
            
            lowestUsedY = min(correctedY,lowestUsedY)
            highestUsedY = max(correctedY, highestUsedY)
            
    if lowestUsedY > 0:
        for i in range(lowestUsedY):
            schematicCubix.pop(0)
            
    if highestUsedY < maxSchematicHeight:
        for i in range(maxSchematicHeight - 1 - highestUsedY):
            schematicCubix.pop()

    schematicHeight = len(schematicCubix)
    schematicLength = length
    schematicWidth = width
    
    for y in range(schematicHeight):
        
        for z in range(schematicLength):
            
            for x in range(schematicWidth):
                
                blockID = schematicCubix[y][z][x]
                
                if "_" in blockID:
                    blockID = blockID.split("_")
                    blockList.append(int(blockID[0]))
                    blockDataList.append(int(blockID[1]))
                    
                else:
                    blockList.append(int(blockID))
                    blockDataList.append(0)
    
    
    #--------Building Tag_Compound-----------
    
    tagHeight = nbt.Tag_Short(name = "Height", shortInt = schematicHeight)
    tagLength = nbt.Tag_Short(name = "Length", shortInt = schematicLength)
    tagWidth = nbt.Tag_Short(name = "Width", shortInt = schematicWidth)
    tagMaterials = nbt.Tag_String(name = "Materials", string = "Alpha")
    tagEntities = nbt.Tag_List(name = "Entities")
    tagTileEntities = nbt.Tag_List(name = "TileEntities")
    tagBlocks = nbt.Tag_Byte_Array(name = "Blocks", arrayOfInts = blockList)
    tagData = nbt.Tag_Byte_Array(name = "Data", arrayOfInts = blockDataList)
    
    return nbt.Tag_Compound(name = "Schematic", listOfTags = [tagHeight,tagLength,tagWidth,tagMaterials,tagEntities,tagTileEntities,tagBlocks,tagData])
    
    
    
    
    
    
    
























































