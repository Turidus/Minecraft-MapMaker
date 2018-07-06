import Parsers
import os


def saveAmountTxT(mapIDMatrix, mapIDList, name):
    
    stringToSave = Parsers.mapIDToAmount(mapIDMatrix, mapIDList)
    
    if not os.path.isdir("./save"):
        os.mkdir("save")
    with open("./save/" + name +"_amount.txt", "w") as saveFile:
        saveFile.write(stringToSave)
        
def saveBlockPositionTxT(mapIDMatrix, mapIDList, name):
    
    stringToSave = Parsers.mapIDToPosition(mapIDMatrix, mapIDList)
    
    if not os.path.isdir("./save"):
        os.mkdir("save")
    with open("./save/" + name +"_BlockPositions.txt", "w") as saveFile:
        saveFile.write(stringToSave)