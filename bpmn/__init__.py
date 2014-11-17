'''
Created on 2011-9-21

@author: hsn
'''
try:
    import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

class XMLFormatError(RuntimeError):
    pass

from bpmn.process import Process

def load_definition(xmlstr):
    root = ElementTree.fromstring(xmlstr)
    processes = []
    for process in root.getchildren():
        processes.append(Process(process))
    return processes
