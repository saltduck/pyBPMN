import uuid
import warnings

from bpmn import engine
from bpmn.exceptions import XMLFormatError
from bpmn.utils import MetaRegister, analyze_node


class BaseElement(object):
    __metaclass__ = MetaRegister

    def __init__(self, tag):
        super(BaseElement, self).__init__()
        self.tagname = tag.tag
        self.id = tag.attrib.get("id", uuid.uuid1().hex)
        engine.db[self.id] = self
        self.children = {}
        for subtag in tag.getchildren():
            element = analyze_node(subtag)
            if element is None:
                continue
            if self.children.has_key(element.id):
                raise XMLFormatError('Duplicate ID!')
            self.children[element.id] = element
        self.setassociation('documentation', Documentation)

    def setassociation(self, attribute, klass, single=False):
        values = [e for e in self.children.values() if isinstance(e, klass)]
        if single:
            if len(values) > 1:
                raise XMLFormatError('There should be only 1 association to {0} in {1}(id={2})'.format(attribute, self.tagname, self.id))
            if len(values) == 0:
                values = None
            else:   # len(values) == 1
                values = values[0]
        setattr(self, attribute, values)


class RootElement(BaseElement):
    def __init__(self, tag):
        super(RootElement, self).__init__(tag)


class Documentation(BaseElement):
    def __init__(self, tag):
        super(Documentation, self).__init__(tag)
        self.text = tag.attrib.get["text"]
        self.textFormat = tag.attrib.get["textFormat"]
