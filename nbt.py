"""Extremly barebone implementation of minecrafts nbt format. The only function it can fullfill is support the generation of
schematic files, implemented are Tag_Compound, Tag_Short, Tag_List, Tag_String Tag_Bytearray, Tag_End"""


class Tag_End():
    
    tagID = 0

class Tag_Short():
    
    def __init__(self, shortInt=None, name=None):
        
        self.shortInt = shortInt
        self.name = name
        self.tagID = 2
        
class Tag_Byte_Array():
    
    def __init__(self, arrayOfInts=None, name=None):
        
        self.arrayOfInts = arrayOfInts
        self.name = name
        self.tagID = 7
        
class Tag_String():
    
    def __init__(self, string=None, name=None):
        
        self.string = string
        self.name = name
        self.tagID = 8
        
class Tag_List():
    
    def __init__(self, name=None):
        
        self.value = 0
        self.name = name
        self.tagID = 9
    


class Tag_Compound():
    
    def __init__(self, listOfTags=None, name=None):
        
        self.listOfTags = listOfTags
        self.name = name
        self.tagID = 10
    
    def tagAppend(self, tag):
        
        if self.listOfTags:
            self.listOfTags.append(tag)
        else:
            self.listOfTags = [tag]

def _stringToTagBytes(string):
    
    
    return _shortIntToTagBytes(len(string)) + bytes(string, "utf8")
    
def _intToBytes(longInt):
    
    if longInt <= 255:
        return bytes([longInt])
    
    rest = longInt % 256
    division = int((longInt - rest) / 256)
    
    return _intToBytes(division) + bytes([rest])
    
def _longIntToTagBytes(longInt):
    
    theBytes = _intToBytes(longInt)

    if len(theBytes) > 4:
        raise ValueError("Maximum Int size is 32 bits")
    
    return bytes(4 - len(theBytes)) + theBytes
    
def _shortIntToTagBytes(shortInt):

    theBytes = _intToBytes(shortInt)
    
    if len(theBytes) > 2:
        raise ValueError("Maximum Int size is 16 bits")
    
    return bytes(2 - len(theBytes)) + theBytes


def toByte(tagCompound):
    
    endByteArray = bytes([tagCompound.tagID]) + _stringToTagBytes(tagCompound.name)
    
    
    for entry in tagCompound.listOfTags:
        
        if entry.tagID == 2:
            
            endByteArray += bytes([2]) + _stringToTagBytes(entry.name) + _shortIntToTagBytes(entry.shortInt)
            
        elif entry.tagID == 7:
            
            endByteArray += bytes([7]) + _stringToTagBytes(entry.name) + _longIntToTagBytes(len(entry.arrayOfInts)) + bytes(entry.arrayOfInts)
            
        elif entry.tagID == 8:
            
            endByteArray += bytes([8]) + _stringToTagBytes(entry.name) + _stringToTagBytes(entry.string)
            
        elif entry.tagID == 9:
            endByteArray += bytes([9]) + _stringToTagBytes(entry.name) + bytes([10]) + _longIntToTagBytes(0)
 
 
    endByteArray += bytes(1)
    
    return endByteArray
     
"""
tC = Tag_Compound(name = "test")
tSt = Tag_String(name = "testString", string = "Hello World")
tSh = Tag_Short(name = "testShort", shortInt = 5)
tBA = Tag_Byte_Array(name = "testByteArray", arrayOfInts = [1,5,3,4])
tL = Tag_List(name ="testList")
tC.listOfTags = [tSh,tBA,tSt]
tC.tagAppend(tL)
toByte(tC)
 """
    
    
    
    
    
    
    
    
    
    
