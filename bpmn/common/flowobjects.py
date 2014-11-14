'''
Created on 2011-9-21

@author: hsn
'''
import logging
logger = logging.getLogger(__file__)
from bpmn.common.baseelement import BaseElement


class FlowObjects(BaseElement):
    def __init__(self,tag):
        super(FlowObjects,self).__init__(tag)
           
    def wait_for_complete(self):
        print "%s<id=%s> is running...".format(
            self.__class__, self.id
            )
    
    def get_next(self):
        return self.next_flowobject
