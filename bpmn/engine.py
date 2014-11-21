import warnings
from nose.tools import eq_
try:
    import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

from .utils import analyze_node

class DataStore(object):
    data = {}
    
    def __getitem__(self, k):
        return self.data[k]

    def __setitem__(self, k ,v):
        self.data[k] = v

    def count(self):
        return len(self.data)

    def clear(self):
        self.data = {}

    def get_event(self, eid):
        from .models.event import Event
        for elem in self.data.values():
            if elem.id == eid and isinstance(elem, Event):
                return elem
        raise KeyError
db = DataStore()

definitions = []
processes = {}

def _analyze_tree(root):
    from models.infrastructure import Definitions
    d = Definitions(root)
    definitions.append(d)
    for cid, child in d.children.items():
        if child.tagname == 'process':
            processes[cid] = child

def load_definition(xmlstr):
    root = ElementTree.fromstring(xmlstr)
    _analyze_tree(root)

def load_definition_file(xmlfile):
    tree = ElementTree.parse(xmlfile)
    root = tree.getroot()
    _analyze_tree(root)
