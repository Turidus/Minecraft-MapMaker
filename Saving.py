import Parsers
import os


def saveAmountTxT(mapIDMatrix, mapIDList, name):
    
    stringToSave = Parsers.mapIDToAmountString(mapIDMatrix, mapIDList)
    
    if not os.path.isdir("./save/" + name + "/"):
        
        if not os.path.isdir("./save"):
            os.mkdir("./save/")
        os.mkdir("./save/" + name + "/")
        
    with open("./save/" + name + "/" + name +"_amount.txt", "w") as saveFile:
        saveFile.write(stringToSave)
        
def saveBlockPositionTxT(positionMatrix, name):
    
    stringToSave = Parsers.positionMatrixToPositionString(positionMatrix)
    
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