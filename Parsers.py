from math import sqrt
from PIL import Image
import os
import io
import sys
import copy
import random as rnd
import threading
import queue
import multiprocessing as mupro

import nbt


_maxThreads = max(1, os.cpu_count() -1)

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
    
    return retString
    
def mapIDToPositionMatrix(mapIDMatrix, minimumY = 6,maximumY = 250):
    
    def _positionWorker():
        
        while True:
        
            input = inQueue.get()
            
            if input == None:
                inQueue.task_done()
                break
            
            elif input[0] == 0:
                
                #Input looks like (flag, list, x coordinate, startY)
                inList = input[1]
                threadLength = len(inList)
                outList = [None for index in range(threadLength)]
                
                for z in range(threadLength):
                    
                    if z == 0:
                        outList[z] = [45,input[2],threadLength - 1,input[3]]
                    
                    else:
                        if int(inList[z]) % 4 == 1:
                            posY = outList[z - 1][3]    
                                        
                        elif int(inList[z]) % 4 == 2:
                            
                            posY = outList[z - 1][3] + 1
                        
                        else:
                            if outList[z - 1][3] <= minimumY:
                                for zDone in range(z):
                                    outList[zDone][3] += 1
                            
                            posY = outList[z - 1][3] - 1
                        
                        
                        outList[z] = [inList[z],input[2], threadLength - (z + 1), posY]
                
                outQueue.put((outList,input[2]))
                inQueue.task_done()
                
            elif input[0] == 1:

                #Input looks like (flag, list, x coordinate, miniumY, maxinum Y)
                inList = input[1]                
                threadLength = len(inList)
                lowestY = input[4]
                
                for z in range(threadLength):
                    
                    lowestY = min(lowestY,inList[z][3])
                    
                if lowestY > input[3]:
                    
                    yOffset = lowestY - input[3]
                    
                    for z in range(threadLength):
                            
                        inList[z][3] -= yOffset
                
                outQueue.put((inList,input[2]))
                inQueue.task_done()
                
                
            elif input[0] == 2:
                
                #Input looks like (flag, list, xCoordinate, miniumY, maxinum Y)
                inList = input[1]
                threadLength = len(inList)
                
                exceedingY = False
                inExceedingRange = False
                rangeZValues = []
                
                for z in range(threadLength):
                    
                    if inList[z][3] > input[4] and not inExceedingRange:
                        exceedingY = True
                        inExceedingRange = True
                        rangeZValues.append(z)
                        
                    elif inList[z][3] <= input[4] and inExceedingRange:
                        inExceedingRange = False
                        rangeZValues.append(z)
                        
                if inExceedingRange:
                    rangeZValues.append(length)
                
                while exceedingY:
                    
                    for index in range(0,len(rangeZValues),2):
                        
                        for z in range(rangeZValues[index],rangeZValues[index + 1]):
                            
                            inList[z][3] -= yMaxOffset
                            
                            
                    exceedingY = False
                    inExceedingRange = False
                    rangeZValues = []
                    
                    for z in range(length):

                        if inList[z][3] > input[4] and not inExceedingRange:
        
                            exceedingY = True
                            inExceedingRange = True
                            rangeZValues.append(z)
                            
                        elif inList[z][3] <= input[4] and inExceedingRange:
                            inExceedingRange = False
                            rangeZValues.append(z)
                            
                    if inExceedingRange:
                        rangeZValues.append(length)
                        
                outQueue.put((inList,input[2]))
                inQueue.task_done()
                
            else:
                inQueue.task_done()
    
    
    
    
    startY = int((maximumY - minimumY) / 2) + minimumY
    
    workMatrix = copy.deepcopy(mapIDMatrix)
    
    #This inserts an additional block at the north end of each North-South line.
    #This is needed to shade the first line of the image correctly.
    for zLine in workMatrix: 
        zLine.insert(0,45)
    
    width = len(workMatrix) 
    length = len(workMatrix[0])
    
    positionMatrix = [[0 for i in range(length)] for i in range(width)]
    
    
    inQueue = mupro.JoinableQueue()
    outQueue = queue.Queue()
    processList = []
    
    for pNum in range(_maxThreads):
        process = mupro.Process(target = _positionWorker)
        process.start()
        processList.append(process)
        
        
    #First pass over the matrix fills it with the position values
    
    for x in range(width):
        
        inQueue.put((0, workMatrix[x], x, startY))
    
    inQueue.join()
    
        
    while not outQueue.empty():
        
        output = outQueue.get()
        positionMatrix[output[1]] = output[0]
                
    #Second pass over the matrix to fix to high Y coordinates
    
    #First Step: Normalisation of each North-South column which are independend from each other,
    #contrary to the West-East rows. At the end, each column has at least one block on
    #the minimal Y coordiante.
    for x in range(width):
        
        inQueue.put((1, positionMatrix[x], x, minimumY, maximumY))
    
    inQueue.join()
    
        
    while not outQueue.empty():
        
        output = outQueue.get()
        positionMatrix[output[1]] = output[0]
        
        
    #Second Step: finding all ranges of blocks in each line that are too high and force them to be lower
    #than the maximum Y coordiante. This can lead to missmatched pixels inside the picture.
    #See Readme for additional information
    yMaxOffset = maximumY - minimumY + 1
    
    for x in range(width):
        
        inQueue.put((2, positionMatrix[x], x, minimumY, maximumY))
    
    inQueue.join()
    
    while not outQueue.empty():
        
        output = outQueue.get()
        positionMatrix[output[1]] = output[0]
                
    
    for process in processList:
        inQueue.put(None)
    for process in processList:
        process.join()
    
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
    
    class Prio():
        prio: int = -1
        
        def add_get(self):
            
            self.prio += 1
            
            return self.prio
    
    def _schematicThreadWorker():
        
        while True:
            threadData = threading.local()
            threadData.input = inQueue.get()
            
            if threadData.input == None:
                inQueue.task_done()
                break
            
            elif threadData.input[0] == 0:
                #Input looks like (flag, prio, rangeY, tulpeRangeZ, tulpeRangeX, tulpeSchematicPosition)

                
            
                threadData.blockList = []
                threadData.blockDataList = []
                
        
                for threadData.yThread in range(threadData.input[2]):
                    
                    for threadData.zThread in range(threadData.input[3][0],threadData.input[3][1]):
                        
                        for threadData.xThread in range(threadData.input[4][0],threadData.input[4][1]):
                            
                            schemLock.acquire()
                            
                            threadData.blockID = schematicCubix[threadData.yThread][threadData.zThread][threadData.xThread]
                            
                            schemLock.release()
                            
                            if "_" in threadData.blockID:
                                threadData.blockID = threadData.blockID.split("_")
                                threadData.blockList.append(int(threadData.blockID[0]))
                                threadData.blockDataList.append(int(threadData.blockID[1]))
                                
                            else:
                                threadData.blockList.append(int(threadData.blockID))
                                threadData.blockDataList.append(0)
                
                
                #--------Building Tag_Compound-----------
                
                threadData.tagList = [
                    nbt.Tag_Short(name = "Height", shortInt = threadData.input[2]),
                    nbt.Tag_Short(name = "Length", shortInt = threadData.input[3][1] - threadData.input[3][0]),
                    nbt.Tag_Short(name = "Width", shortInt = threadData.input[4][1] - threadData.input[4][0]),
                    nbt.Tag_String(name = "Materials", string = "Alpha"),
                    nbt.Tag_List(name = "Entities"),
                    nbt.Tag_List(name = "TileEntities"),
                    nbt.Tag_Byte_Array(name = "Blocks", arrayOfInts = threadData.blockList),
                    nbt.Tag_Byte_Array(name = "Data", arrayOfInts = threadData.blockDataList)
                ]
                
                threadData.tagCompoundName = str(threadData.input[5][0]) + " " + str(threadData.input[5][1])
                
                outPrioQueue.put((threadData.input[1], nbt.Tag_Compound(name = threadData.tagCompoundName, listOfTags = threadData.tagList)))
                
                inQueue.task_done()
            
   
   
    maxSchematicHeight = maxY - minY
    highestUsedY = minY
    length = len(positionMatrix[0])
    width = len(positionMatrix)
    
    
    #In the schematicCubix, x and z positions are switched, because the way schematics are build
    schematicCubix = [ [["0" for i in range(width)] for i in range(length)] for i in range(maxSchematicHeight + 1)]

    
    for x in range(width):
        
        for z in range(length):
            position = positionMatrix[x][z]
            
            correctedY = position[3] - minY

            schematicCubix[correctedY][z][x] = mapIDDic[position[0]][2]

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
    priority = Prio()
    
    inQueue = queue.Queue()
    outPrioQueue = queue.PriorityQueue()
    threadList = []
    schemLock = threading.Lock()
    
    for tNum in range(_maxThreads):
        thread = threading.Thread(target = _schematicThreadWorker)
        thread.start()
        threadList.append(thread)
    
    
    for rangeZ in range(1,len(lengthRanges)):
        
        for rangeX in range(1,len(widthRanges)):
            lengthRange = (lengthRanges[rangeZ-1] , lengthRanges[rangeZ])
            widthRange = (widthRanges[rangeX-1] , widthRanges[rangeX])
            schematicPosition = (rangeZ - 1, rangeX - 1)
            inQueue.put((0, priority.add_get(), schematicHeight, lengthRange, widthRange, schematicPosition))
    
    
    inQueue.join()
    
    for thread in threadList:
        inQueue.put(None)
    for thread in threadList:
        thread.join()
    
    while not outPrioQueue.empty():
        
        output = outPrioQueue.get()

        tag_compound_list.append(output[1])

        outPrioQueue.task_done()
    
    tc = tag_compound_list[0]
    

    return tag_compound_list
    
    
    
    
    
    
    
























































