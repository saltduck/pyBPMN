'''
Created on 2011-9-21

@author: hsn
'''
from . import ThrowEvent


class EndEvent(ThrowEvent):
    def __init__(self, tag):
        super(EndEvent,self).__init__(tag)
