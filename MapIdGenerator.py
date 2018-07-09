def mult180(x):
    return int((x * 180) / 255)
    
def mult220(x):
    return int((x * 220) / 255)

def mapIDGenerator3D(blackList = []):
    
    with open("BaseColorIds.txt","r") as baseIDFile:
        baseIDList = baseIDFile.read().splitlines()
    
    mapIDList = []
    baseIDList.pop(0)
    
    for entry in baseIDList:
        entry = entry.split("\t")
        if blackList != None and entry[0] in blackList:
            continue
        
        rgbList = entry[1].split(",")
        
        rgbList180 = (mult180(int(rgbList[0])), mult180(int(rgbList[1])), mult180(int(rgbList[2])))
        rgbList220 = (mult220(int(rgbList[0])), mult220(int(rgbList[1])), mult220(int(rgbList[2])))
        rgbList255 = (int(rgbList[0]), int(rgbList[1]), int(rgbList[2]))
        
        mapIDList.append([int(entry[0]) * 4, rgbList180, entry[2], entry[3]])
        mapIDList.append([int(entry[0]) * 4 + 1, rgbList220, entry[2], entry[3]])
        mapIDList.append([int(entry[0]) * 4 + 2, rgbList255, entry[2], entry[3]])
    
    
    return mapIDList

def mapIDGenerator2D(blackList = []):
    
    with open("BaseColorIds.txt","r") as baseIDFile:
        baseIDList = baseIDFile.read().splitlines()
    
    mapIDList = []
    baseIDList.pop(0)
    
    for entry in baseIDList:
        entry = entry.split("\t")
        if blackList != None and entry[0] in blackList:
            continue
        
        rgbList = entry[1].split(",")
        
        rgbList220 = (mult220(int(rgbList[0])), mult220(int(rgbList[1])), mult220(int(rgbList[2])))
        
        mapIDList.append([int(entry[0]) * 4 + 1, rgbList220, entry[2], entry[3]])
    
    
    return mapIDList