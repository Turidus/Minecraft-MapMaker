"""
Provides funcions to transform the differnent data representations into each other.

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

from math import sqrt
from PIL import Image
import io
import copy

import nbt



def _rgbDistance(rgbFromPixel,rgbFromList):
    
    rDif = rgbFromPixel[0] - rgbFromList[0]
    gDif = rgbFromPixel[1] - rgbFromList[1]
    bDif = rgbFromPixel[2] - rgbFromList[2]
    
    return sqrt( rDif ** 2 + gDif ** 2 + bDif ** 2)


def _openImage(pathString):
    
    try:
        with open(pathString,"rb") as file: 
            img = Image.open(io.BytesIO(file.read()))
    
    except(IOError):
        raise IOError("File is not a (supported) image")
    
    return img
    
            
def _sortkeyForUsedBlocks(string):
    
    if "_" not in string:        
        return (int(string), -1)
    else:
        splitString = string.split("_")
        return (int(splitString[0]),int(splitString[1]))
        
        
    
    
def imageFileToRGBMatrix(pathString):
    
    img = _openImage(pathString)

    if img.size[0] == 0 or img.size[1] == 0:
        raise IOError("Input image was empty")
        
    if img.mode != "RGB":
        
        img = img.convert("RGB")
    
    
    rgbMatrix  = []
    
    for x in range(img.height):
        
        tempLine = []
        
        for z in range(img.width):
            
            tempLine.append(img.getpixel((x,z)))
        
        rgbMatrix.append(tempLine)
        
    return rgbMatrix
    
def rgbMatrixToMapID(rgbMatrix, mapIDDic):
    
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
            
            for entry in mapIDDic:
                
                tempDif = _rgbDistance(rgbMatrix[x][z],mapIDDic[entry][0])

                if tempDif < curDif:
                    
                    curDif = tempDif
                    curMapID = entry
            
            knownResults[rgbMatrix[x][z]] = curMapID
            mapIdMatrix[x][z] = curMapID

    return mapIdMatrix

def mapIDToAmountString(mapIDMatrix,mapIDDic):
    
    usedBlocks = {}
    
    for x in range(len(mapIDMatrix)):
        
        
        
        for z in range(len(mapIDMatrix[x])):
            
            block = mapIDDic[mapIDMatrix[x][z]]
            
            if block[2] not in usedBlocks:
                
                usedBlocks[block[2]] = [1,block[1]]
            
            else:
                usedBlocks[block[2]][0] += 1
    
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
        
    if "9" in usedBlocks:
        glassBlocks = 5 * usedBlocks["9"][0]
        retString += "\n{:^40}{:^10}{:>10}\n".format("for Water, aprox. Glass:", "20", str(glassBlocks))
    
    return retString
    

    
def mapIDToPositionMatrix(mapIDMatrix, minimumY = 6,maximumY = 250):
    
    positionMatrix = []
    startY = int((maximumY - minimumY) / 2) + minimumY
    
    workMatrix = copy.deepcopy(mapIDMatrix)
    
    #This inserts an additional block at the north end of each North-South line.
    #This is needed to shade the first line of the image correctly.
    for zLine in workMatrix: 
        zLine.insert(0,45)
    
    width = len(workMatrix) 
    length = len(workMatrix[0])
    
    positionMatrix = [[0 for i in range(length)] for i in range(width)]

    for x in range(width):
        
        
        for z in range(length):
            
            if z == 0:
                positionMatrix[x][z] = [45,x,length - 1,startY]
            
            else:
                if int(workMatrix[x][z]) % 4 == 1:
                    posY = positionMatrix[x][z-1][3]    
                                  
                elif int(workMatrix[x][z]) % 4 == 2:
                    
                    posY = positionMatrix[x][z-1][3] + 1
                
                else:
                    if positionMatrix[x][z-1][3] <= minimumY:
                        for position in positionMatrix[x][:z]:
                            position[3] += 1
                    
                    posY = positionMatrix[x][z-1][3] - 1
                
                
                positionMatrix[x][z] = [workMatrix[x][z],x, length - (z + 1), posY]


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

    

    
def positionMatrixToPositionString(positionMatrix,mapIDDic):
    
    retString = "{:^40}({:^5},{:^5},{:^5})\n".format("Block","X","Z","Y")
    
    for x in range(len(positionMatrix)):
        
        for z in range(len(positionMatrix[0])):
            
            position = positionMatrix[x][z]
            retString += "{:^40}({:^5},{:^5},{:^5})\n".format(mapIDDic[position[0]][1],position[1], position[2],position[3])
    
    return retString



def mapIDToPicture(mapIDMatrix, mapIDDic):
    

    image = Image.new("RGB", (len(mapIDMatrix),len(mapIDMatrix[0])))
    
    for x in range(len(mapIDMatrix)):
        
        for z in range(len(mapIDMatrix[0])):
            
            image.putpixel((x,z), mapIDDic[mapIDMatrix[x][z]][0])
            
    return image
    

    return tag_compound_list




def positionMatrixToTag_CompoundList(positionMatrix, mapIDDic, minY, maxY, maxSize):
    
    maxSchematicHeight = maxY - minY
    highestUsedY = minY
    length = len(positionMatrix[0])
    width = len(positionMatrix)
    
    
    
    schematicCubix = [ [["0" for i in range(width)] for i in range(length)] for i in range(maxSchematicHeight + 1)]
    
    
    for x in range(width):
        
        for z in range(length):
            position = positionMatrix[x][z]
            
            correctedY = position[3] - minY
            
            schematicCubix[correctedY][z][x] = mapIDDic[position[0]][2]
            
            #Adding glass around water
            
            if mapIDDic[position[0]][2] == "9":
                
                try:
                    if schematicCubix[correctedY - 1][z][x] == "0":
                        schematicCubix[correctedY - 1][z][x] = "20"
                except IndexError:
                    pass
                    
                try:
                    if schematicCubix[correctedY][z - 1][x] == "0":
                        schematicCubix[correctedY][z - 1][x] = "20"
                except IndexError:
                    pass
                    
                try:
                    if schematicCubix[correctedY][z + 1][x] == "0":
                        schematicCubix[correctedY][z + 1][x] = "20"
                except IndexError:
                    pass
                    
                try:
                    if schematicCubix[correctedY][z][x - 1] == "0":
                        schematicCubix[correctedY][z][x - 1] = "20"
                except IndexError:
                    pass
                
                try:
                    if schematicCubix[correctedY][z][x + 1] == "0":
                        schematicCubix[correctedY][z][x + 1] = "20"
                except IndexError:
                    pass

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
            
            tagList = [
                nbt.Tag_Short(name = "Height", shortInt = schematicHeight),
                nbt.Tag_Short(name = "Length", shortInt = lengthRanges[rangeZ] - lengthRanges[rangeZ - 1]),
                nbt.Tag_Short(name = "Width", shortInt = widthRanges[rangeX] - widthRanges[rangeX - 1]),
                nbt.Tag_String(name = "Materials", string = "Alpha"),
                nbt.Tag_List(name = "Entities"),
                nbt.Tag_List(name = "TileEntities"),
                nbt.Tag_Byte_Array(name = "Blocks", arrayOfInts = blockList),
                nbt.Tag_Byte_Array(name = "Data", arrayOfInts = blockDataList),
            ]
            
            tag_compound_list.append(nbt.Tag_Compound(name = str(rangeZ - 1) + " " + str(rangeX - 1), listOfTags = tagList))
    
    
    return tag_compound_list
    
    
    
    
























































