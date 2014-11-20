import warnings
try:
    import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree


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
        from .event import Event
        for elem in self.data.values():
            if elem.id == eid and isinstance(elem, Event):
                return elem
        raise KeyError
db = DataStore()

processes = {}

def _analyze_tree(root):
    from .process import Process
    from .common import Resource
    for tag in root.getchildren():
        if tag.tag == 'process':
            process = Process(tag)
            processes[process.id] = process
        elif tag.tag == 'resource':
            Resource(tag)
        else:
            warnings.warn('{0} is unknown'.format(tag.tag))

def load_definition(xmlstr):
    root = ElementTree.fromstring(xmlstr)
    _analyze_tree(root)

def load_definition_file(xmlfile):
    tree = ElementTree.parse(xmlfile)
    root = tree.getroot()
    _analyze_tree(root)
