import Parsers
import os
import nbt
import gzip


def saveAmountTxT(mapIDMatrix, mapIDList, name):
    
    stringToSave = Parsers.mapIDToAmountString(mapIDMatrix, mapIDList)
    
    if not os.path.isdir("./save/" + name + "/"):
        
        if not os.path.isdir("./save"):
            os.mkdir("./save/")
        os.mkdir("./save/" + name + "/")
        
    with open("./save/" + name + "/" + name +"_amount.txt", "w") as saveFile:
        saveFile.write(stringToSave)
        
def saveBlockPositionTxT(positionMatrix,mapIDList, name):
    
    stringToSave = Parsers.positionMatrixToPositionString(positionMatrix,mapIDList)
    
    if not os.path.isdir("./save/" + name):
        
        if not os.path.isdir("./save"):
            os.mkdir("./save/")
        os.mkdir("./save/" + name + "/")
        
    with open("./save/" + name + "/" + name +"_BlockPositions.txt", "w") as saveFile:
        saveFile.write(stringToSave)
        
def saveImage(mapIDMatrix, mapIDList, name):
    
    imageToSave = Parsers.mapIDToPicture(mapIDMatrix, mapIDList)
    
    if not os.path.isdir("./save/" + name):
        
        if not os.path.isdir("./save"):
            os.mkdir("./save/")
        os.mkdir("./save/" + name + "/")
    
    with open("./save/" + name + "/" + name +"_endresult.bmp", "wb") as saveFile:
        
        imageToSave.save(saveFile, format = "BMP")
        
def saveSchematic(Tag_Compound, name):
    
    schematicToSave = gzip.compress(nbt.toByte(Tag_Compound))
    
    if not os.path.isdir("./save/" + name):
        
        if not os.path.isdir("./save"):
            os.mkdir("./save/")
        os.mkdir("./save/" + name + "/")
        
    with open("./save/" + name + "/" + name +".schematic", "wb") as saveFile:
        
        saveFile.write(schematicToSave)
        
    
    
    