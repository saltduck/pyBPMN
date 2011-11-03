'''
Created on 2011-9-21

@author: hsn
'''
from baseelement import BaseElement


class FlowObjects(BaseElement):
    def __init__(self,tag):
        super(FlowObjects,self).__init__(tag)
           
    def wait_for_complete(self):
        pass
    
    def get_next(self):
        return self.next_flowobject