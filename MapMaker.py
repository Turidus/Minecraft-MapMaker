import Parsers
import Saving
import pickle
import os

try:
    with open("MapColorIDs","rb") as file:
        mapIdList = pickle.load(file)
except IOError:
    print("Missing MapColorIDs file")

rgbMatrix = Parsers.imageFileToRGBMatrix("test4.jpg")
mapIdMatrix = Parsers.rgbMatrixToMapID(rgbMatrix,mapIdList)

Saving.saveAmountTxT(mapIdMatrix,mapIdList,"test4")
Saving.saveBlockPositionTxT(mapIdMatrix, mapIdList, "test4")



    