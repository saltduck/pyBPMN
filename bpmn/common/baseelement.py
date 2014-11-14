'''
Created on 2011-9-21

@author: hsn
'''
class BaseElement(object):
    def __init__(self,tag):
        self.id = tag.attrib.get("id", "")
        self.name = tag.attrib.get("name", "")
