'''
Created on 2011-9-21

@author: hsn
'''
from . import Event


class CatchEvent(Event):
    def __init__(self, tag):
        super(CatchEvent,self).__init__(tag)
        self.parallelMultiple = tag.get("parallelMultiple", False)
        self.outputSet = tag.get("outputSet", None)
