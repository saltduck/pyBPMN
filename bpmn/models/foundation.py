import logging
logger = logging.getLogger(__file__)
import uuid
import warnings

from bpmn import engine
from bpmn.exceptions import XMLFormatError
from bpmn.core import MetaRegister, StringAttribute, BooleanAttribute, MultiAssociation, XMLTagText
from bpmn.utils import analyze_node


class XMLBaseElement(object):
    __metaclass__ = MetaRegister

    def __init__(self, tag):
        super(XMLBaseElement, self).__init__()
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


class BaseElement(XMLBaseElement):
    id = StringAttribute('id', default=lambda : uuid.uuid1().hex)
    documentation = MultiAssociation('Documentation')


class RootElement(BaseElement):
    pass
        

class ReferenceElement(BaseElement):
    refid = XMLTagText()


class Documentation(BaseElement):
    text = StringAttribute('text', required=True)
    textFormat = StringAttribute('textFormat', required=True)


class Relationship(BaseElement):
    type = StringAttribute('type', required=True)
    direction = StringAttribute('direction')
    source = MultiAssociation('Source', required=True)
    target = MultiAssociation('Target', required=True)


class Source(XMLBaseElement):
    ref = StringAttribute('ref', required=True)


class Target(XMLBaseElement):
    ref = StringAttribute('ref', required=True)


class Extension(XMLBaseElement):
    definition = StringAttribute('definition')
    mustUnderstand = BooleanAttribute('mustUnderstand', False)
    documentation = MultiAssociation('Documentation')
