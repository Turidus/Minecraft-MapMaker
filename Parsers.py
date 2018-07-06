import math
from PIL import Image
import io
import sys

def _rgbDistance(rgbFromPixel,rgbFromList):
    rDif = rgbFromPixel[0] - rgbFromList[0]
    gDif = rgbFromPixel[1] - rgbFromList[1]
    bDif = rgbFromPixel[2] - rgbFromList[2]
    
    return math.sqrt( rDif ** 2 + gDif ** 2 + bDif ** 2)
    
def blockFinder(mapID,mapIdList):
    
    for entry in mapIdList:
        
        if entry[0] == mapID:
            return entry[2:]
            
def openImage(pathString):
    
    try:
        with open(pathString,"rb") as file: 
            img = Image.open(io.BytesIO(file.read()))
    
    except(IOError):
        raise IOError("pathString does not exist or is not a (supported) image")
    
    return img
    
def addOneToAllY(positionMatrix):
    for z in range(0,len(positionMatrix),1):
        for x in range(0,len(positionMatrix[z]),1):
            positionMatrix[z][x][3] += 1
    
def imageFileToRGBMatrix(pathString):
    
    img = openImage(pathString)
    
    if img.mode != "RGB":
        
        img = img.convert("RGB")
    
    
    rgbMatrix  = []
    
    for y in range(0,img.width,1):
        
        tempLine = []
        
        for x in range(0,img.height,1):
            
            tempLine.append(img.getpixel((x,y)))
        
        rgbMatrix.append(tempLine)
    
    return rgbMatrix
    
def rgbMatrixToMapID(rgbMatrix, mapIdList):
    
    mapIdMatrix = []
    curRGB = (-1,-1,-1)
    curMapID = "0"
    
    
    for y in range(0,len(rgbMatrix),1):
        
        tempLine = []
        
        for x in range(0,len(rgbMatrix[y]),1):
            
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

def mapIDToAmount(mapIDMatrix,mapIdList):
    
    usedBlocks = {}
    
    for y in range(0,len(mapIDMatrix),1):
        
        
        
        for x in range(0,len(mapIDMatrix[y]),1):
            
            block = blockFinder(mapIDMatrix[y][x],mapIdList)
            
            if block[0] not in usedBlocks:
                
                usedBlocks[block[0]] = [1,block[1]]
            
            else:
                usedBlocks[block[0]][0] += 1
    
    retString = "You need follwing amount of blocks\n"
    retString += "{:^40}{:^10}{:^10}\n".format("Blockname","BlockID","Amount")
    
    for key in usedBlocks:
        
        if "_" in usedBlocks[key][1]:
            blockID =  usedBlocks[key][1].replace("_",":")
        
        else:
            blockID =  usedBlocks[key][1]
            
        retString += "{:^40}{:^10}{:^10}\n".format(key, blockID, str(usedBlocks[key][0]))
    
    return retString
    
def mapIDToPosition(mapIDMatrix,mapIdList):
    
    positionMatrix = []
    curMapID = "44"
    curBlock = "Cobbelstone"
    startY = 64
    
    
    height = len(mapIDMatrix) + 1
    
    if (height - 1) > 0:
        width = len(mapIDMatrix[0])
    else:
        raise ValueError("mapIDMatrix was empty")
    
    zeroLine = [] #This adds a additinal row of blocks into the map, to shade the first row of the image correctly
                    
    
    for zeroPosition in range(0,width,1):
        zeroLine.append("44")
    mapIDMatrix.insert(0,zeroLine)
    
    
    for z in range(0,height,1):
        
        tempLine = []
        
        for x in range(0,width,1):
            
            if z == 0:
                tempLine.append(["44",x,height,startY])
            
            else:
                if int(mapIDMatrix[z][x]) % 4 == 0:
                    posY = positionMatrix[z-1][x][3] - 1
                    if posY < 0:
                        addOneToAllY(positionMatrix)
                        for item in tempLine:
                            item[3] += 1
                        posY = 0
                
                elif int(mapIDMatrix[z][x]) % 4 == 2:
                    posY = positionMatrix[z-1][x][3] + 1
                
                else:
                    posY = positionMatrix[z-1][x][3]
                
                tempLine.append([mapIDMatrix[z][x],x, height - z, posY])
        
        positionMatrix.append(tempLine)
    
    retString = "{:^40}({:^5},{:^5},{:^5})\n".format("Block","X","Z","Y")
    
    for z in range(0,len(positionMatrix),1):
        for x in range(0,len(positionMatrix[z]),1):
            if positionMatrix[z][x][0] != curMapID:
                curMapID = positionMatrix[z][x][0]
                curBlock = blockFinder(curMapID,mapIdList)[0]
                
            retString += "{:^40}({:^5},{:^5},{:^5})\n".format(curBlock,positionMatrix[z][x][1] + 1,positionMatrix[z][x][2],positionMatrix[z][x][3])
    
    return retString































































