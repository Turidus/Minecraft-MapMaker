"""
Generates the mapColorID dictionary out of the BaseColorIDList.txt and a optional blacklist.

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

def mult180(x):
    return int((x * 180) / 255)
    
def mult220(x):
    return int((x * 220) / 255)
    
def mult135(x):
    return int((x * 135) / 255)

def mapColorIDGenerator3D(blackList = []):
    """
    Generates the mapColorID dictionary for all blocks NOT specified in the blackList.
    These means there are three mapColorIDs generated for every entry left in BaseColorID.txt
    Contains all colors that can be archived ingame.
    
    param: blackList: A list of BaseColorID strings (f.e. ["33", "22", "5"])
    """
    

    with open("BaseColorIds.txt","r") as baseIDFile:
        baseIDList = baseIDFile.read().splitlines()
    
    mapColorIDDic = {}
    baseIDList.pop(0)
    
    for entry in baseIDList:
        entry = entry.split("\t")
        if blackList != None and entry[0] in blackList:
            continue
        
        rgbList = entry[1].split(",")
        
        rgbList180 = (mult180(int(rgbList[0])), mult180(int(rgbList[1])), mult180(int(rgbList[2])))
        rgbList220 = (mult220(int(rgbList[0])), mult220(int(rgbList[1])), mult220(int(rgbList[2])))
        rgbList255 = (int(rgbList[0]), int(rgbList[1]), int(rgbList[2]))
        
        mapColorIDDic[int(entry[0]) * 4] = (rgbList180, entry[2], entry[3])
        mapColorIDDic[int(entry[0]) * 4 + 1] = (rgbList220, entry[2], entry[3])
        mapColorIDDic[int(entry[0]) * 4 + 2] = (rgbList255, entry[2], entry[3])
    
    
    return mapColorIDDic

def mapColorIDGenerator2D(blackList = []):
    """
    Generates the flat mapColorID dictionary for all blocks NOT specified in the blackList.
    These means there is one mapColorID generated for every entry left in BaseColorID.txt
    Contains all colors that can be archived ingame with a flat construct.
    
    param: blackList: A list of BaseColorID strings (f.e. ["33", "22", "5"])
    """
    
    with open("BaseColorIds.txt","r") as baseIDFile:
        baseIDList = baseIDFile.read().splitlines()
    
    mapColorIDDic = {}
    baseIDList.pop(0)
    
    for entry in baseIDList:
        entry = entry.split("\t")
        if blackList != None and entry[0] in blackList:
            continue
        
        rgbList = entry[1].split(",")
        
        rgbList220 = (mult220(int(rgbList[0])), mult220(int(rgbList[1])), mult220(int(rgbList[2])))
        
        mapColorIDDic[int(entry[0]) * 4 + 1] = (rgbList220, entry[2], entry[3])
    
    return mapColorIDDic
    
def mapColorIDGenerator4Colors(blackList = []):
    """
    Generates the full mapColorID dictionary for all blocks NOT specified in the blackList.
    These means there are three mapColorIDs generated for every entry left in BaseColorID.txt
    Contains all possible colors a map can display.
    
    param: blackList: A list of BaseColorID strings (f.e. ["33", "22", "5"])
    """
    

    with open("BaseColorIds.txt","r") as baseIDFile:
        baseIDList = baseIDFile.read().splitlines()
    
    mapColorIDDic = {}
    baseIDList.pop(0)
    
    for entry in baseIDList:
        entry = entry.split("\t")
        if blackList != None and entry[0] in blackList:
            continue
        
        rgbList = entry[1].split(",")
        
        rgbList180 = (mult180(int(rgbList[0])), mult180(int(rgbList[1])), mult180(int(rgbList[2])))
        rgbList220 = (mult220(int(rgbList[0])), mult220(int(rgbList[1])), mult220(int(rgbList[2])))
        rgbList255 = (int(rgbList[0]), int(rgbList[1]), int(rgbList[2]))
        rgbList135 = (mult135(int(rgbList[0])), mult135(int(rgbList[1])), mult135(int(rgbList[2])))
        
        mapColorIDDic[int(entry[0]) * 4] = (rgbList180, entry[2], entry[3])
        mapColorIDDic[int(entry[0]) * 4 + 1] = (rgbList220, entry[2], entry[3])
        mapColorIDDic[int(entry[0]) * 4 + 2] = (rgbList255, entry[2], entry[3])
        mapColorIDDic[int(entry[0]) * 4 + 3] = (rgbList13, entry[2], entry[3])