'''
Created on 2011-9-21

@author: hsn
'''
from . import ConnectingObjects

class SequenceFlow(ConnectingObjects):
    def __init__(self, tag):
        super(SequenceFlow,self).__init__(tag)
        self.source_id = tag.attrib["sourceRef"]
        self.target_id = tag.attrib["targetRef"]
