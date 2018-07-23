from appJar import gui
import MapMaker
import re
import os
import queue
import time


class Args():
    
    pathToImage = None
    bl = None
    name = None
    twoD = False
    p = True
    bp = True
    ba = True
    s = True
    minY = 4
    maxY = 250
    maxS = 129
    
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
            app.queueFunction(app.setMessage, "output", errorString + "\nStatus: Waiting\n")
        else:
            app.queueFunction(app.setMessage,"output", "Status: Done\n\nStatus: Waiting\n")
            
        app.queueFunction(app.enableButton,"Go")
        
def _collectOutput(outPrioQueue):
        
    #oldMessage = app.queueFunction(app.getMessage,"output") #---- Does not work

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

            app.queueFunction(app.setMessage,"output", oldMessage + "\nStatus: " + out[1] + "\n")
            
            outPrioQueue.task_done()
        if out[1] == "Finished with this image":
            break
            
        
    
    

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
        
    
    arguments.bl = entries["bl"]
    if arguments.bl == "For example: 33, 14, 5" or arguments.bl == "":
        arguments.bl = None
    
    elif "a" in re.sub(r'[^0-9,\s]','a',arguments.bl):
        errorHappend = True
        errorString +="Error: Invalid blacklist\n"
        
    else:
        arguments.bl = arguments.bl.replace(" ", "")
        arguments.bl = arguments.bl.split(",")
    
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
    
    arguments.twoD = boxes["2D"]
    
    arguments.p = boxes["Picture"]
    
    arguments.bp = boxes["Block positions"]
    
    arguments.ba = boxes["Block amount"]
    
    arguments.s = boxes["Schematic"]
    
    
    app.setMessage("output", "Status: Running. This can take awhile\n")
    
    outQueue = queue.PriorityQueue()    
    app.thread(_dispatchMapMaker,arguments, outQueue)
    app.thread(_collectOutput, outQueue)
    


    


#---Building the GUI----
app = gui("Minecraft Map Maker")
app.setSize("1000x600")

#---Column 0
app.setSticky("w")
app.addLabel("pathToImage","Path to image",row = 1, column = 0)
app.setLabelAlign("pathToImage","e")

app.addLabel("bl","Base color IDs that\nshould not be used",row = 2, column = 0)
app.setLabelAlign("bl","e")

app.addLabel("n","Name",row = 3, column = 0)
app.setLabelAlign("n","e")

#---Column 1
app.setSticky("w")

app.addFileEntry("pathToImage",row = 1, column = 1)
#app.setEntry("pathToImage", "Path to the image")
app.setEntryTooltip("pathToImage", "The path to your image")

app.addEntry("bl", row = 2, column = 1)
app.setEntryTooltip("bl", "For example: 33, 14, 5\nSee Readme for more infos")
#app.setEntry("bl", "For example: 33, 14, 5")

app.addEntry("n", row = 3, column = 1)
app.setEntryTooltip("n", "optional")


#---Column 2

app.setPadding(1)
app.setSticky("")
app.addVerticalSeparator(row = 0, column = 2, rowspan = 6)



#---Column 3
app.setSticky("w")
app.addLabel("switches","Switches", row = 0, column = 3)
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
app.addLabel("ints","Dimensions", row = 0, column = 5)
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
#app.setMessageAspect("output", 1000)
app.setMessageWidth("output", 1000)
#app.setMessageHeight("output", 100)
app.setMessageBg("output", "white")
app.setMessageRelief("output", "solid")
app.setMessageAlign("output", "w")

#---Row 8
app.setSticky("we")
app.addButton("Go", press, row = 7, column = 0)
app.addButton("Exit", press, row = 7, column = 5)



app.go()