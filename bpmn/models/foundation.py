import logging
logger = logging.getLogger(__file__)
import uuid
import warnings

from bpmn import engine
from bpmn.exceptions import XMLFormatError
from bpmn.core import MetaRegister, StringAttribute, MultiAssociation
from bpmn.utils import analyze_node


class BaseElement(object):
    __metaclass__ = MetaRegister
    id = StringAttribute('id', default=lambda : uuid.uuid1().hex)
    documentation = MultiAssociation('Documentation')

    def __init__(self, tag):
        super(BaseElement, self).__init__()
        self.tag = tag
        self.tagname = tag.tag
        self.children = {}
        for subtag in tag.getchildren():
            element = analyze_node(subtag)
            if element is None:
                continue
            if self.children.has_key(element.id):
                raise XMLFormatError('Duplicate ID!')
            self.children[element.id] = element
        for attrname, attr in self.attributes.items():
            setattr(self, attrname, attr.getvalue(self))
        engine.db[self.id] = self
        self.validate()
        del self.tag    # Just used for attr.getvalue()

    def validate(self):
        pass


class RootElement(BaseElement):
    pass


class Documentation(BaseElement):
    text = StringAttribute('text', required=True)
    textFormat = StringAttribute('textFormat', required=True)
