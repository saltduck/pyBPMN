try:
    import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree


class DataStore(object):
    data = {}
    
    def __setitem__(self, k ,v):
        self.data[k] = v

    def get_event(self, eid):
        from .event import Event
        for elem in self.data.values():
            if elem.id == eid and isinstance(elem, Event):
                return elem
        raise KeyError
db = DataStore()

processes = {}

def load_definition(xmlstr):
    from .process import Process
    root = ElementTree.fromstring(xmlstr)
    for tag in root.getchildren():
        process = Process(tag)
        processes[process.id] = process

def trigger(eventid):
    db.get_event(eventid).trigger()

