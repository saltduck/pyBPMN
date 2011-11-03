'''
Created on 2011-9-21

@author: hsn
'''
from catchEvent import CatchEvent


class EndEvent(CatchEvent):
    def __init__(self, tag):
        super(EndEvent,self).__init__(tag)