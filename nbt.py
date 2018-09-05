"""
Extremly barebone implementation of Minecrafts NBT format.
The only function it can fullfill is support the generation of schematic files and map.dat files.

WARNING: This implemention violates the reference by treating the TAGs as UNsigned and can not deal with negativ numbers
         or positiv numbers greater than the maximum signed value of that format.

Implemented are Tag_End, Tag_Byte, Tag_Short, Tag_Int, Tag_Bytearray, Tag_List, Tag_String, Tag_Compound


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


class Tag_End():
    
    tagID = 0

class Tag_Byte():
    
    def __init__(self, byteInt=None, name=None):
        
        self.byteInt = byteInt
        self.name = name
        self.tagID = 1

class Tag_Short():
    
    def __init__(self, shortInt=None, name=None):
        
        self.shortInt = shortInt
        self.name = name
        self.tagID = 2
        
class Tag_Int():
    
    def __init__(self, fullInt=None, name=None):
        
        self.fullInt = fullInt
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
    
    
def _intToBytes(Int):
    
    if Int <= 255:
        return bytes([Int])
    
    rest = Int % 256
    division = int(Int / 256)
    
    return _intToBytes(division) + bytes([rest])
    
    
def _fullIntToTagBytes(fullInt):
    
    theBytes = _intToBytes(fullInt)

    if len(theBytes) > 4:
        raise ValueError("Maximum full Int size is 32 bits")
    
    return bytes(4 - len(theBytes)) + theBytes
    
    
def _shortIntToTagBytes(shortInt):

    theBytes = _intToBytes(shortInt)
    
    if len(theBytes) > 2:
        raise ValueError("Maximum short Int size is 16 bits")
    
    return bytes(2 - len(theBytes)) + theBytes
    
    
def _byteIntToTagBytes(byteInt):

    theBytes = _intToBytes(byteInt)
    
    if len(theBytes) > 1:
        raise ValueError("Maximum byte Int size is 8 bits")
    
    return theBytes


def toByte(tagCompound):
    
    endByteArray = bytes([tagCompound.tagID]) + _stringToTagBytes(tagCompound.name)
    
    
    for entry in tagCompound.listOfTags:
        
        if entry.tagID == 1:
            
            endByteArray += bytes([1]) + _stringToTagBytes(entry.name) + _byteIntToTagBytes(entry.byteInt)
        
        elif entry.tagID == 2:
            
            endByteArray += bytes([2]) + _stringToTagBytes(entry.name) + _shortIntToTagBytes(entry.shortInt)
            
        elif entry.tagID == 3:
            
            endByteArray += bytes([3]) + _stringToTagBytes(entry.name) + _fullIntToTagBytes(entry.fullInt)
            
        elif entry.tagID == 7:
            
            endByteArray += bytes([7]) + _stringToTagBytes(entry.name) + _fullIntToTagBytes(len(entry.arrayOfInts)) + bytes(entry.arrayOfInts)
            
        elif entry.tagID == 8:
            
            endByteArray += bytes([8]) + _stringToTagBytes(entry.name) + _stringToTagBytes(entry.string)
            
        elif entry.tagID == 9:
            endByteArray += bytes([9]) + _stringToTagBytes(entry.name) + bytes([10]) + _fullIntToTagBytes(0)
 
 
    endByteArray += bytes(1)
    
    return endByteArray
    
    
    
    
    
    
    
    
    
    
