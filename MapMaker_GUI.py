"""
Builds and displays the GUI for Minecraft Map Maker.

Based on appJar.


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


from appJar import gui
import os
import queue
import time
from urllib.request import urlopen
from urllib.error import URLError
import json

import MapMaker


class Args():
    
    pathToImage = None
    bl = []
    name = None
    twoD = False
    p = True
    bp = True
    ba = True
    s = True
    minY = 4
    maxY = 250
    maxS = 129
    v = False
    
arguments = Args()

def _dispatchMapMaker(args, outPrioQueue):
    
    errorHappend = False
    errorString = ""
    
    try:
        MapMaker.MapMaker(args, outPrioQueue)
        
    except IOError as ioErr:
        errorHappend = True
        errorString += str(ioErr) + "\n"
    
    except ValueError as vErr:
        errorHappend = True
        errorString += str(vErr) + "\n"
        
    finally:
        if errorHappend:
            print(errorString)
            outPrioQueue.put( (-2, "Error: " + errorString + "\nStatus: Waiting\n") )
        else:
            outPrioQueue.put( (-1, "Status: Done\n\nStatus: Waiting\n") )
            
            
        app.queueFunction(app.enableButton,"Go")
        
def _collectOutput(outPrioQueue):
    

    oldMessage = app.getMessage("output")   #Not thread safe
    out = (0,"Waiting")
    waitString = ""
    
    while True:
        
        
        if outPrioQueue.empty():
            if len(waitString) > 5:
                waitString = " ."
            else:
                waitString += " ."
                
            app.queueFunction(app.setMessage,"output", oldMessage + "\nStatus: " + out[1] + waitString + "\n")
        
            time.sleep(0.5)
        
        else:
            out = outPrioQueue.get()

            if out[0] < 0:
                app.queueFunction(app.setMessage,"output", out[1] + "\n")
                outPrioQueue.task_done()
                break
                
            else:
                app.queueFunction(app.setMessage,"output", oldMessage + "\nStatus: " + out[1] + "\n")
                outPrioQueue.task_done()
            
       

def press(name):
    
    if name == "Exit":
        app.stop()
    
    app.disableButton("Go")
    
    errorHappend = False
    errorString = ""
        
    entries = app.getAllEntries()
    boxes = app.getAllCheckBoxes()
    

    arguments.pathToImage = os.path.abspath(entries["pathToImage"])
    if not os.path.isfile(arguments.pathToImage):
        errorHappend = True
        errorString += "Error: File not found\n"
        
    
    arguments.n = entries["n"]
    if arguments.n == "":
        arguments.n = None
    
    try:
        arguments.minY = int(entries["minY"])
        if arguments.minY < 0 or arguments.minY > 251: raise ValueError("minY is not valid\n")
        
        arguments.maxY = int(entries["maxY"])
        if arguments.maxY < 4 or arguments.maxY > 251: raise ValueError("maxY is not valid\n")
        
        if arguments.maxY - arguments.minY < 4: raise ValueError("minY and maxY are to close (<4)\n")
        
        app.setValidationEntry("minY")
        app.setValidationEntry("maxY")
        
    except ValueError as vErr:
        errorHappend = True
        errorString += str(vErr)
        if str(vErr) == "minY is not valid\n":
            app.setValidationEntry("minY", state = "invalid")
            
        elif str(vErr) == "maxY is not valid\n":
            app.setValidationEntry("maxY", state = "invalid")
        
        else:
            app.setValidationEntry("minY", state = "invalid")
            app.setValidationEntry("maxY", state = "invalid")

    try:
        arguments.maxS = int(entries["maxS"])
        if arguments.maxS < 1: raise ValueError("maxS is not valid\n")
        app.setValidationEntry("maxS")
        
    except ValueError as vErr:
        errorHappend = True
        errorString += str(vErr)
        app.setValidationEntry("maxS", state = "invalid")
        
    if errorHappend:
        app.setMessage("output", errorString + "Status: Waiting\n")
        app.enableButton("Go")
        return
        
    for item in boxes:
        
        if not boxes[item] and len(item) > 3 and item[:3] == "ID:":
            colorID = item.split()[1]
            arguments.bl.append(colorID)
    
    arguments.twoD = boxes["2D"]
    
    arguments.p = boxes["Picture"]
    
    arguments.bp = boxes["Block positions"]
    
    arguments.ba = boxes["Block amount"]
    
    arguments.s = boxes["Schematic"]
    
    
    app.setMessage("output", "Status: Running. This can take awhile\n")
    
    outQueue = queue.PriorityQueue()    
    app.thread(_dispatchMapMaker,arguments, outQueue)
    app.thread(_collectOutput, outQueue)


def colorListOpen():
    app.showSubWindow("CB")
    
def colorListClose():
    app.hideSubWindow("CB")
    
def updateCheck():
    
    version = app.getLabel("version").split(" ")[1].strip()
    
    try:
        with urlopen("https://api.github.com/repos/Turidus/Minecraft-MapMaker/releases/latest") as response:
            
            jsondata = response.read().decode("utf-8")
            
    except URLError:
        
        app.errorBox("Error", "Could not connect to Github")
        
    jsonDic = json.loads(jsondata)
    lastRelease = jsonDic["tag_name"].strip()
    
    if version == lastRelease:
        app.infoBox("No update", "This Version is up to date")
    else:
        app.infoBox("A update", "There is an new version\nTo update, go to latest release")
    
def aboutMenu(name):
    
    if name == "About":
        app.showSubWindow("about")
        



#---Building the GUI----
#---Main Window----
app = gui("Minecraft Map Maker", showIcon = False)
app.setIcon("icon.gif")
app.setSize("1000x600")
app.addMenuList("About",["About"],aboutMenu)

#---Column 0
app.setSticky("w")
app.addLabel("pathToImage","Path to image",row = 1, column = 0)
app.setLabelAlign("pathToImage","e")

app.addLabel("n","Name",row = 2, column = 0)
app.setLabelAlign("n","e")

app.addLabel("bl","Colors/Blocks used",row = 3, column = 0)
app.setLabelAlign("bl","e")


#---Column 1
app.setSticky("w")

app.addFileEntry("pathToImage",row = 1, column = 1)
app.setEntryTooltip("pathToImage", "The path to your image")

app.addEntry("n", row = 2, column = 1)
app.setEntryTooltip("n", "optional")

app.addButton("Colors/Blocks", colorListOpen, row = 3, column = 1)


#---Column 2

app.setPadding(1)
app.setSticky("")
app.addVerticalSeparator(row = 0, column = 2, rowspan = 6)



#---Column 3
app.setSticky("w")
app.addLabel("generate","Generate:", row = 0, column = 3)
app.addCheckBox("2D", row = 1, column = 3)
app.setCheckBoxTooltip("2D", "Generate a 2D instead of a stepped construced. Only 53 colors.")

app.addCheckBox("Picture", row = 2, column = 3)
app.setCheckBox("Picture")
app.setCheckBoxTooltip("Picture", "Generate a preview picture")

app.addCheckBox("Block positions", row = 3, column = 3)
app.setCheckBox("Block positions")
app.setCheckBoxTooltip("Block positions", "Generate a txt file with all blocks an their positions")


app.addCheckBox("Block amount", row = 4, column = 3)
app.setCheckBox("Block amount")
app.setCheckBoxTooltip("Block amount", "Generate a txt file with all blocks and the amount needed")

app.addCheckBox("Schematic", row = 5, column = 3)
app.setCheckBox("Schematic")
app.setCheckBoxTooltip("Schematic", "Generate a schematic file for compatible plugins")


#---Column 4
app.setSticky("")
app.addVerticalSeparator(row = 0, column = 4, rowspan = 6)
app.setPadding(0)

#---Column 5
app.setSticky("w")
app.addLabel("ints","Dimensions:", row = 0, column = 5)
app.addLabel("minY","Minimal Y coordiante",row = 1, column = 5)
app.setLabelAlign("minY","e")
app.addLabel("maxY","Maximum Y coordiante",row = 2, column = 5)
app.setLabelAlign("maxY","e")
app.addLabel("maxS","Maxium Schematic size",row = 3, column = 5)
app.setLabelAlign("maxS","e")

#---Column 6
app.setSticky("w")

app.addValidationEntry("minY", row = 1, column = 6)
app.setEntry("minY", "4")
app.setEntryMaxLength("minY", 3)
app.setEntryWidth("minY", 5)
app.setEntryTooltip("minY", "At least 0, at most 251. Needs to be 4 smaller than maxY")

app.addValidationEntry("maxY", row = 2, column = 6)
app.setEntry("maxY", "250")
app.setEntryMaxLength("maxY", 3)
app.setEntryWidth("maxY", 5)
app.setEntryTooltip("maxY", "At least 4, at most 255. Needs to be 4 bigger than minY")

app.addValidationEntry("maxS", row = 3, column = 6)
app.setEntry("maxS", "129")
app.setEntryMaxLength("maxS", 5)
app.setEntryWidth("maxS", 5)
app.setEntryTooltip("maxS", "At least 1. The bigger maxS becomes, the bigger the impact of pasting the schematic")


#---Row 7
app.setSticky("we")
app.addMessage("output", "Status: Waiting\n", row = 6, column = 0, colspan = 7)
app.setMessageWidth("output", 1000)
app.setMessageBg("output", "white")
app.setMessageRelief("output", "solid")
app.setMessageAlign("output", "w")

#---Row 8
app.setSticky("we")
app.addButton("Go", press, row = 7, column = 0)
app.addButton("Exit", press, row = 7, column = 5)



#------------Subwindow-CB-------------
app.startSubWindow("CB", modal = True)

try:
    with open("BaseColorIds.txt","r") as baseIDFile:
        baseIDList = baseIDFile.read().splitlines()
        baseIDList.pop(0)
except IOError:
    app.setMessage("output", "Error: No BaseColorID file found. Please exit and check your installation")

app.setSticky("w")
app.setPadding(2,2)
columnLength = 15

for index in range(len(baseIDList)):
    lineSplit = baseIDList[index].split("\t")
    boxName = "ID: {:<3}{:<30}".format(lineSplit[0],lineSplit[2])
    boxColor = lineSplit[1].split(", ")
    boxColorHex = "#%0.2x%0.2x%0.2x" % (int(boxColor[0]),int(boxColor[1]),int(boxColor[2]))
    
    colPic = int(index / columnLength) * 2
    col = colPic + 1
    row = index % columnLength
    app.addLabel(boxName, text = "", row = row, column = colPic)
    app.setLabelBg(boxName, boxColorHex)
    app.setLabelRelief(boxName, "solid")
    app.setLabelWidth(boxName, 5)
    app.addCheckBox(boxName, row = row, column = col)
    app.setCheckBox(boxName)
    

app.addButton("Back", colorListClose, row = columnLength + 1)
app.addWebLink("Colors and their assoicated blocks (Minecraft Wiki)", "https://minecraft.gamepedia.com/Map_item_format", column = 1, row = columnLength + 1)
app.stopSubWindow()

#------------Subwindow-about-------------
app.startSubWindow("about")
app.setPadding(1,1)
app.addLabel("Made by: Turidus")
app.addWebLink("Readme", "https://github.com/Turidus/Minecraft-MapMaker/blob/master/README.md")
app.addWebLink("Sourcecode", "https://github.com/Turidus/Minecraft-MapMaker")
app.addWebLink("Latest Release", "https://github.com/Turidus/Minecraft-MapMaker/releases/latest")

with open("version") as vFile:
    app.addLabel("version", text = vFile.readline())
    
app.addButton("Check for Update", updateCheck)

app.stopSubWindow()


if __name__ == "__main__":
    app.go()