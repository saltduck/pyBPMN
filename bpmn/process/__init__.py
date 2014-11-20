'''
Created on 2011-9-21

@author: hsn
'''

import logging
import copy
import warnings
from threading import Thread

from bpmn.common import FlowElementsContainer, CallableElement
from bpmn import models

 
class Process(FlowElementsContainer, CallableElement):
    """ Process Class """
    def __init__(self, root):
        super(Process, self).__init__(root)
        self.processType = root.get("processType", "none")
        self.isClosed = root.get("isClosed", False)
        self.isExecutable = root.get("isExecutable", True)
        for element in self.children.values():
            if hasattr(element, 'process_refs'):
                element.process_refs(self.children)
        self.instances = []
        
    def element_count(self):
        return len(self.objects)
    
    def instantiate(self):
        assert self.isExecutable
        instance = ProcessInst(self)
        self.instances.append(instance)
        instance.start()
        return instance

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
        self.tokens = set([e for e in process.children.values() if e.auto_instantiate])
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
            immutable_tokens = list(self.tokens)
            for elem in immutable_tokens:
                inst = elem.instantiate()
                inst.wait_for_complete()
                self.tokens.discard(elem)
                self.tokens.update(inst.get_next()) 
        # process instance has completed
        self.is_running = False
        self.is_finished = True
        
    def alive(self):
        return self.is_running
