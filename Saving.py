"""
Provides functions that save the different data representations to disc

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

import os
import gzip

import Parsers
import nbt


def saveAmountTxT(mapIDMatrix, mapIDDic, name):
    
    stringToSave = Parsers.mapIDToAmountString(mapIDMatrix, mapIDDic)
    
    if not os.path.isdir("./save/" + name + "/"):
        
        if not os.path.isdir("./save"):
            os.mkdir("./save/")
        os.mkdir("./save/" + name + "/")
        
    with open("./save/" + name + "/" + name +"_amount.txt", "w") as saveFile:
        saveFile.write(stringToSave)
        
def saveBlockPositionTxT(positionMatrix,mapIDDic, name):
    
    stringToSave = Parsers.positionMatrixToPositionString(positionMatrix,mapIDDic)
    
    if not os.path.isdir("./save/" + name):
        
        if not os.path.isdir("./save"):
            os.mkdir("./save/")
        os.mkdir("./save/" + name + "/")
        
    with open("./save/" + name + "/" + name +"_BlockPositions.txt", "w") as saveFile:
        saveFile.write(stringToSave)
        
def saveImage(mapIDMatrix, mapIDDic, name):
    
    imageToSave = Parsers.mapIDToPicture(mapIDMatrix, mapIDDic)
    
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
    
    
    