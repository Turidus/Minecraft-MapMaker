from appJar import gui
import MapMaker
import re
import os


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

def press(name):
    
    if name == "Exit":
        app.stop()
        
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
        return
    
    arguments.twoD = boxes["2D"]
    
    arguments.p = boxes["Picture"]
    
    arguments.bp = boxes["Block positions"]
    
    arguments.ba = boxes["Block amount"]
    
    arguments.s = boxes["Schematic"]
    
    try:
        app.setMessage("output", "Status: Running. This can take awhile\n")
        MapMaker.MapMaker(arguments)
        
    except IOError as ioErr:
        errorHappend = True
        errorString += str(ioErr) + "\n"
    
    except ValueError as vErr:
        errorHappend = True
        errorString += str(vErr) + "\n"
        
    finally:
        if errorHappend:
            print(errorString)
            app.setMessage("output", errorString + "\nStatus: Waiting\n")
        else:
            app.setMessage("output", "Status: Done\n\nStatus: Waiting\n")
        
        
        
        
        


#---Building the GUI----
app = gui("Minecraft Map Maker")
app.setSize("1000x600")

#---Column 0
app.setSticky("we")
app.addLabel("pathToImage","Path to image:",row = 1, column = 0)
app.addLabel("bl","Base color IDs that\nshould not be used:",row = 2, column = 0)
app.addLabel("n","Optional name:",row = 3, column = 0)

#---Column 1
app.setSticky("we")

app.addFileEntry("pathToImage",row = 1, column = 1)
app.setEntry("pathToImage", "Path to the image")

app.addEntry("bl", row = 2, column = 1)
app.setEntry("bl", "For example: 33, 14, 5")

app.addEntry("n", row = 3, column = 1)


#---Column 2

app.setPadding(1)
app.setSticky("")
app.addVerticalSeparator(row = 0, column = 2, rowspan = 6)



#---Column 3
app.setSticky("w")
app.addLabel("switches","Switches", row = 0, column = 3)
app.addCheckBox("2D", row = 1, column = 3)

app.addCheckBox("Picture", row = 2, column = 3)
app.setCheckBox("Picture")

app.addCheckBox("Block positions", row = 3, column = 3)
app.setCheckBox("Block positions")

app.addCheckBox("Block amount", row = 4, column = 3)
app.setCheckBox("Block amount")

app.addCheckBox("Schematic", row = 5, column = 3)
app.setCheckBox("Schematic")


#---Column 4
app.setSticky("")
app.addVerticalSeparator(row = 0, column = 4, rowspan = 6)
app.setPadding(0)

#---Column 5
app.setSticky("ew")
app.addLabel("minY","Minimal Y coordiante:",row = 1, column = 5)
app.addLabel("maxY","Maximum Y coordiante:",row = 2, column = 5)
app.addLabel("maxS","Maxium Schematic size:",row = 3, column = 5)

#---Column 6
app.setSticky("ew")
app.addLabel("ints","Dimensions", row = 0, column = 6)
app.addValidationEntry("minY", row = 1, column = 6)
app.setEntry("minY", "4")

app.addValidationEntry("maxY", row = 2, column = 6)
app.setEntry("maxY", "250")

app.addValidationEntry("maxS", row = 3, column = 6)
app.setEntry("maxS", "129")


#---Row 7
app.setSticky("w")
app.addMessage("output", "Status: Waiting\n", row = 6, column = 0, colspan = 7)
#app.setMessageAspect("output", 1000)
app.setMessageWidth("output", 1000)
app.setMessageBg("output", "white")

#---Row 8
app.addButton("Go", press, row = 7, column = 0)
app.addButton("Exit", press, row = 7, column = 4) 




app.go()