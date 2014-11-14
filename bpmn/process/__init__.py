'''
Created on 2011-9-21

@author: hsn
'''

import logging
try:
    import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

from bpmn.common.flowobjects import FlowObjects
from bpmn.event.startEvent import StartEvent
from bpmn.event.endEvent import EndEvent
from bpmn.activity.scripttask import ScriptTask
from bpmn.connectingobjects.sequenceflow import SequenceFlow

 
KNOWNTAGS = {
            'startEvent'    : StartEvent,
            'endEvent'      : EndEvent,
            'scriptTask'    : ScriptTask,
            'sequenceFlow'  : SequenceFlow
        }
        

class ProcessDef(object):
    """ Process Definition Class """
    def __init__(self, xmlstr):
        self.root = ElementTree.fromstring(xmlstr)

    def new(self):
        return Process(self.root.getchildren()[0])
        

class Process(object):
    """ Process Class """
    def __init__(self, root):
        self.id = root.attrib["id"]
        self.name = root.attrib["name"]
        self.processType = root.get("processType", "private")
        self.isClosed = root.get("isClosed", False)
        self.isExcecutable = root.get("isExecutable", True)
        self.objects = {}
        for subtag in root.getchildren():
            tagname = subtag.tag
            try:
                tagclass = KNOWNTAGS[tagname]
            except KeyError:
                continue
            element = tagclass(subtag)
            if isinstance(element, FlowObjects):
                self.objects[element.id] = element
            if isinstance(element, SequenceFlow):
                self.objects[element.source_id].next_flowobject_id = element.target_id
        for element in self.objects.values():
            if hasattr(element, 'next_flowobject_id'):
                element.next_flowobject = self.objects[element.next_flowobject_id]
        self.result = None
        self.tokens = self.get_all_startEvent()
        self.is_running = False
        self.is_finished = False
    
    @property
    def token(self):
        if len(self.tokens) == 1:
            return self.tokens[0]
        raise AttributeError, "Process instance has no attribute 'token'"
        
    def element_count(self):
        return len(self.objects)
    
    def get_all_startEvent(self):
        result = []
        for element in self.objects.values():
            if isinstance(element, StartEvent):
                result.append(element)
        return result
    
    def start(self):
        self.is_running = True
        while self.tokens:
            for i in range(len(self.tokens)):
                self.tokens[i].wait_for_complete()
                self.tokens[i] = self.tokens[i].get_next()
            # remove ended tokens
            self.tokens = filter(lambda e:not isinstance(e, EndEvent), self.tokens)
        self.is_running = False
        self.is_finished = True
        
    def alive(self):
        return self.is_running
