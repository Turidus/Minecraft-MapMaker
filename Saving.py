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
        
def saveSchematic(Tag_Compound_List, name):
    
    if not os.path.isdir("./save/" + name):
        
        if not os.path.isdir("./save"):
            os.mkdir("./save/")
        os.mkdir("./save/" + name + "/")
    
    if len(Tag_Compound_List) == 1:
        Tag_Compound_List[0].name = "Schematic"
        schematicToSave = gzip.compress(nbt.toByte(Tag_Compound_List[0]))
            
        with open("./save/" + name + "/" + name +".schematic", "wb") as saveFile:
            
            saveFile.write(schematicToSave)
            
    else:
        for index in range(len(Tag_Compound_List)):
            
            tempTag_Compound = Tag_Compound_List[index]
            partNumber = tempTag_Compound.name.split()
            tempTag_Compound.name = "Schematic"
            
            schematicToSave = gzip.compress(nbt.toByte(Tag_Compound_List[index]))
                
            with open("./save/" + name + "/" + name +"partX{}Z{}.schematic".format(partNumber[0],partNumber[1]), "wb") as saveFile:
                
                saveFile.write(schematicToSave)
    
    
    