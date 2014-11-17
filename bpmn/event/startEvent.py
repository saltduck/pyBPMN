'''
Created on 2011-9-21

@author: hsn
'''
from . import CatchEvent


class StartEvent(CatchEvent):
    def __init__(self, tag):
        super(StartEvent,self).__init__(tag)
        self.isInterrupting = tag.attrib.get("isInterrupting", False)
