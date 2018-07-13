"""Extremly barebone implementation of minecrafts nbt format. The only function it can fullfill is the generation of
schematic files"""

import gzip

class Tag_Compound():
    
    def __init__(self, value=None, name=None):
        
        self.value = value
        self.name = name
        self.tagID = 10
        

        
    

