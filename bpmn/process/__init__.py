'''
Created on 2011-9-21

@author: hsn
'''

import logging
import copy
import warnings
from threading import Thread

from bpmn.common import FlowElementsContainer, CallableElement
from bpmn.common import SequenceFlow, FlowNode
from bpmn.event.startEvent import StartEvent
from bpmn.event.endEvent import EndEvent
from bpmn.activity import Activity
from bpmn.activity.scripttask import ScriptTask

 
KNOWNTAGS = {
            'startEvent'    : StartEvent,
            'endEvent'      : EndEvent,
            'scriptTask'    : ScriptTask,
            'sequenceFlow'  : SequenceFlow
        }
        

class GlobalTask(CallableElement):
    pass


class Process(FlowElementsContainer, CallableElement):
    """ Process Class """
    def __init__(self, root):
        super(Process, self).__init__(root)
        self.processType = root.get("processType", "none")
        self.isClosed = root.get("isClosed", False)
        self.isExecutable = root.get("isExecutable", True)
        self.objects = {}
        for subtag in root.getchildren():
            tagname = subtag.tag
            try:
                tagclass = KNOWNTAGS[tagname]
            except KeyError:
                warnings.warn('{0} is not implemented'.format(tagname))
                continue
            element = tagclass(subtag)
            self.append(element)
            if hasattr(element, "id"):
                self.objects[element.id] = element
        for element in self.objects.values():
            if hasattr(element, 'process_refs'):
                element.process_refs(self.objects)
        self.instances = []
        
    def element_count(self):
        return len(self.objects)
    
    def instantiate(self):
        assert self.isExecutable
        instance = ProcessInst(self)
        self.instances.append(instance)
        instance.start()

    def join(self):
        for instance in self.instances:
            instance.join()
            self.instances.remove(instance)


class ProcessInst(Thread):
    """ Runtime Process Instance """
    def __init__(self, process):
        super(ProcessInst, self).__init__()
        self.process = process
        self.state = "none"
        self.tokens = [e for e in process.objects.values() if e.auto_instantiate]
        self.is_running = False
        self.is_finished = False

    @property
    def token(self):
        if len(self.tokens) == 1:
            return self.tokens[0]
        raise AttributeError, "Process instance has no attribute 'token'"
    
    def run(self):
        self.is_running = True
        while self.tokens:
            for i in range(len(self.tokens)):
                self.tokens[i].instantiate()
                self.tokens[i].wait_for_complete()
                self.tokens[i] = self.tokens[i].get_next()
            # remove ended tokens
            self.tokens = filter(lambda e:not isinstance(e, EndEvent), self.tokens)
        self.is_running = False
        self.is_finished = True
        
    def alive(self):
        return self.is_running
