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
    

    raise IOError
    
def _mapIDThreadWorker():
    pass
            
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
    
    for x in range(img.height):
        
        tempLine = []
        
        for z in range(img.width):
            
            tempLine.append(img.getpixel((x,z)))
        
        rgbMatrix.append(tempLine)
        
    return rgbMatrix
    
def rgbMatrixToMapID(rgbMatrix, mapIdList):
    
    length = len(rgbMatrix[0])
    width = len(rgbMatrix)
    
    mapIdMatrix = [[0 for i in range(length)] for i in range(width)]
    
    knownResults = {}

    for x in range(width):
        
        for z in range(length):
            
            if rgbMatrix[x][z] in knownResults:
                mapIdMatrix[x][z] = knownResults[rgbMatrix[x][z]]
                continue
            
            curDif = 450
            
            for entry in mapIdList:
                
                tempDif = _rgbDistance(rgbMatrix[x][z],entry[1])

                if tempDif < curDif:
                    
                    curDif = tempDif
                    curMapID = entry[0]
            
            knownResults[rgbMatrix[x][z]] = curMapID
            mapIdMatrix[x][z] = curMapID

    return mapIdMatrix

def mapIDToAmountString(mapIDMatrix,mapIdList):
    
    usedBlocks = {}
    
    for x in range(len(mapIDMatrix)):
        
        
        
        for z in range(len(mapIDMatrix[x])):
            
            block = _blockFinder(mapIDMatrix[x][z],mapIdList)
            
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
    startY = int((maximumY - minimumY) / 2) + minimumY
    
    workMatrix = copy.deepcopy(mapIDMatrix)
    
    #This inserts an additional block at the north end of each North-South line.
    #This is needed to shade the first line of the image correctly.
    for zLine in workMatrix: 
        zLine.insert(0,45)
    
    width = len(workMatrix) 
    length = len(workMatrix[0])
    

    for x in range(width):
        
        tempLine = []
        
        for z in range(length):
            
            if z == 0:
                tempLine.append([45,x,length - 1,startY])
            
            else:
                if int(workMatrix[x][z]) % 4 == 1:
                    posY = tempLine[-1][3]    
                                  
                elif int(workMatrix[x][z]) % 4 == 2:
                    
                    posY = tempLine[-1][3] + 1
                
                else:
                    if tempLine[-1][3] <= minimumY:
                        for position in tempLine:
                            position[3] += 1
                    
                    posY = tempLine[-1][3] - 1
                
                
                tempLine.append([workMatrix[x][z],x, length - (z + 1), posY])
                
                
        positionMatrix.append(tempLine)


    #Second pass over the matrix to fix to high Y coordinates
    
    #First Step: Normalisation of each North-South column which are independend from each other,
    #contrary to the West-East rows. At the end, each column has at least one block on
    #the minimal Y coordiante.
    for x in range(width):
        lowestY = maximumY
        
        for z in range(length):
            
            lowestY = min(lowestY,positionMatrix[x][z][3])
            
        if lowestY > minimumY:
            
            yOffset = lowestY - minimumY
            
            for z in range(length):
                    
                positionMatrix[x][z][3] -= yOffset
        
    #Second Step: finding all ranges of blocks in each line that are too high and force them to be lower
    #than the maximum Y coordiante. This can lead to missmatched pixels inside the picture.
    #See Readme for additional information
    yMaxOffset = maximumY - minimumY + 1
    
    for x in range(width):
        exceedingY = False
        inExceedingRange = False
        rangeZValues = []
        
        for z in range(length):
            
            if positionMatrix[x][z][3] > maximumY and not inExceedingRange:
                exceedingY = True
                inExceedingRange = True
                rangeZValues.append(z)
                
            elif positionMatrix[x][z][3] <= maximumY and inExceedingRange:
                inExceedingRange = False
                rangeZValues.append(z)
                
        if inExceedingRange:
            rangeZValues.append(length)
        
        while exceedingY:
            
            for index in range(0,len(rangeZValues),2):
                
                for z in range(rangeZValues[index],rangeZValues[index + 1]):
                    
                    positionMatrix[x][z][3] -= yMaxOffset
                    
                    
            exceedingY = False
            inExceedingRange = False
            rangeZValues = []
            
            for z in range(length):
                
                if positionMatrix[x][z][3] > maximumY and not inExceedingRange:

                    exceedingY = True
                    inExceedingRange = True
                    rangeZValues.append(z)
                    
                elif positionMatrix[x][z][3] <= maximumY and inExceedingRange:
                    inExceedingRange = False
                    rangeZValues.append(z)
                    
            if inExceedingRange:
                rangeZValues.append(length)
    
    return positionMatrix

    

    
def positionMatrixToPositionString(positionMatrix,mapIDList):
    
    curMapID = 45
    curBlock = "Cobbelstone"
    retString = "{:^40}({:^5},{:^5},{:^5})\n".format("Block","X","Z","Y")
    
    for x in range(len(positionMatrix)):
        for z in range(len(positionMatrix[0])):
            if positionMatrix[x][z][0] != curMapID:
                curMapID = positionMatrix[x][z][0]
                curBlock = _blockFinder(curMapID,mapIDList)[0]
                
            retString += "{:^40}({:^5},{:^5},{:^5})\n".format(curBlock,positionMatrix[x][z][1], positionMatrix[x][z][2],positionMatrix[x][z][3])
    
    return retString



def mapIDToPicture(mapIDMatrix, mapIDList):
    
    curMapID = 0
    curRGB = (0,0,0)

    image = Image.new("RGB", (len(mapIDMatrix),len(mapIDMatrix[0])))
    
    for x in range(len(mapIDMatrix)):
        
        for z in range(len(mapIDMatrix[0])):
            
            if curMapID != mapIDMatrix[x][z]:
                
                for item in mapIDList:
                    
                    if item[0] == mapIDMatrix[x][z]:
                        
                        curRGB = item[1]
                        break
            
            image.putpixel((x,z),curRGB)
            
    return image
    


def positionMatrixToTag_CompoundList(positionMatrix, mapIDList, minY, maxY, maxSize):
    
    maxSchematicHeight = maxY - minY
    highestUsedY = minY
    length = len(positionMatrix[0])
    width = len(positionMatrix)
    curMapID = 0
    curBlockID = 0
    
    
    
    schematicCubix = [ [["0" for i in range(width)] for i in range(length)] for i in range(maxSchematicHeight + 1)]
    
    
    for x in range(width):
        
        for z in range(length):
            
            if positionMatrix[x][z][0] != curMapID:
                curMapID = positionMatrix[x][z][0]
                curBlockID = _blockFinder(curMapID,mapIDList)[1]


            correctedY = positionMatrix[x][z][3] - minY
            schematicCubix[correctedY][z][x] = curBlockID
            highestUsedY = max(correctedY, highestUsedY)
            
    if highestUsedY < maxSchematicHeight:
        for i in range(maxSchematicHeight - 1 - highestUsedY):
            schematicCubix.pop()

    #Preparing data for building the Tag_Compounds.
    #If the picture is bigger than maxSize, it will get cut in pices
    #to make importing them easier. 
    #Even so, you should use Fast asynchrone world edit or similar.
    #See Readme for additional information
    
    schematicHeight = len(schematicCubix)
    schematicLength = length
    schematicWidth = width
    
    lengthRanges = []
    for i in range(int(schematicLength / maxSize) + 1):
        lengthRanges.append(i * maxSize)
    if lengthRanges[-1] < schematicLength:
        lengthRanges.append(schematicLength)
    
    widthRanges = []
    for i in range(int(schematicWidth / maxSize) + 1):
        widthRanges.append(i * maxSize)
    if widthRanges[-1] < schematicWidth:
        widthRanges.append(schematicWidth)
    tag_compound_list = []
    
    for rangeZ in range(1,len(lengthRanges)):
        
        for rangeX in range(1,len(widthRanges)):
            
            blockList = []
            blockDataList = []
    
            for y in range(schematicHeight):
                
                for z in range(lengthRanges[rangeZ - 1],lengthRanges[rangeZ]):
                    
                    for x in range(widthRanges[rangeX - 1],widthRanges[rangeX]):
                        
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
            tagLength = nbt.Tag_Short(name = "Length", shortInt = lengthRanges[rangeZ] - lengthRanges[rangeZ - 1])
            tagWidth = nbt.Tag_Short(name = "Width", shortInt = widthRanges[rangeX] - widthRanges[rangeX - 1])
            tagMaterials = nbt.Tag_String(name = "Materials", string = "Alpha")
            tagEntities = nbt.Tag_List(name = "Entities")
            tagTileEntities = nbt.Tag_List(name = "TileEntities")
            tagBlocks = nbt.Tag_Byte_Array(name = "Blocks", arrayOfInts = blockList)
            tagData = nbt.Tag_Byte_Array(name = "Data", arrayOfInts = blockDataList)
            tagList = [tagHeight,tagLength,tagWidth,tagMaterials,tagEntities,tagTileEntities,tagBlocks,tagData]
            
            tag_compound_list.append(nbt.Tag_Compound(name = str(rangeZ - 1) + " " + str(rangeX - 1), listOfTags = tagList))
    return tag_compound_list
    
    
    
    
    
    
    
























































