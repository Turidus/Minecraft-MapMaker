import pickle

def mult180(x):
    return int((x * 180) / 255)
    
def mult220(x):
    return int((x * 220) / 255)

mapIdList = []

with open("BaseColorIds.txt","r") as baseIdFile:
    baseIdString = baseIdFile.read()
    baseIdList = baseIdString.splitlines()

baseIdList.pop(0)
for entry in baseIdList:
    entry = entry.split("\t")
    rgbList = entry[1].split(",")
    
    rgbList180 = [mult180(int(rgbList[0])), mult180(int(rgbList[1])), mult180(int(rgbList[2]))]
    rgbList220 = [mult220(int(rgbList[0])), mult220(int(rgbList[1])), mult220(int(rgbList[2]))]
    rgbList255 = [int(rgbList[0]), int(rgbList[1]), int(rgbList[2])]
    
    mapIdList.append([int(entry[0]) * 4, rgbList180, entry[2], entry[3]])
    mapIdList.append([int(entry[0]) * 4 + 1, rgbList220, entry[2], entry[3]])
    mapIdList.append([int(entry[0]) * 4 + 2, rgbList255, entry[2], entry[3]])

for entry in mapIdList:
    if "\xa0" in entry[2]:
        
        tempList = entry[2].split("\xa0")
        tempString  = ""
        
        for item in tempList:
            tempString += item + " "
        
        
        entry[2] = tempString.rstrip()

with open("MapColorIDs","bw") as mapIdFile:
    pickle.dump(mapIdList,mapIdFile)
        