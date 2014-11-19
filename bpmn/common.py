import logging
logger = logging.getLogger(__file__)
from . import engine
from .foundation import BaseElement, RootElement

def make_bool(boolstr):
    boolstr = boolstr.lower()
    if boolstr in ('true', 'yes'):
        return True
    return False


class FlowElement(BaseElement):
    auto_instantiate = False

    def __init__(self, tag):
        super(FlowElement, self).__init__(tag)
        self.name = tag.attrib.get("name", "")

    def instantiate(self):
        return self


class SequenceFlow(FlowElement):
    def __init__(self, tag):
        super(SequenceFlow, self).__init__(tag)
        self.source_id = tag.attrib["sourceRef"]
        self.target_id = tag.attrib["targetRef"]
        self.isImmediate = tag.attrib.get("isImmediate", False)

    def process_refs(self, objects):
        self.sourceRef = objects[self.source_id]
        self.targetRef = objects[self.target_id]
        assert isinstance(self.sourceRef, FlowNode)
        assert isinstance(self.targetRef, FlowNode)
        self.targetRef.incoming.append(self)
        self.sourceRef.outgoing.append(self)


class FlowNode(FlowElement):
    def __init__(self, tag):
        super(FlowNode, self).__init__(tag)
        self.incoming = []
        self.outgoing = []
           
    def wait_for_complete(self):
        print "{0}<id={1}> is running...".format(
            self.__class__, self.id
            )
    
    def get_next(self):
        return [outgoing.targetRef for outgoing in self.outgoing]
    

class Expression(SequenceFlow):
    pass


class FlowElementsContainer(BaseElement):
    def __init__(self, *args, **kwargs):
        super(FlowElementsContainer, self).__init__(*args, **kwargs)
        self.flowElements = []

    def append(self, element):
        """ add FlowElement object into self """
        assert getattr(element, "container", None) is None
        self.flowElements.append(element)
        element.container = self

class ItemDefinition(RootElement):
    pass


class Message(RootElement):
    def __init__(self, tag):
        super(Message, self).__init__(tag)
        self.name = tag.attrib["name"]


class Resource(RootElement):
    def __init__(self, tag):
        super(Resource, self).__init__(tag)
        self.name = tag.attrib["name"]
        self.resourceParameters = []
        for subtag in tag.getchildren():
            if subtag.tag == 'resourceParameter':
                self.resourceParameters.append(ResourceParameter(subtag))


class ResourceParameter(BaseElement):
    def __init__(self, tag):
        super(ResourceParameter, self).__init__(tag)
        self.name = tag.attrib["name"]
        self.isRequired = make_bool(tag.attrib["isRequired"])
        

class CallableElement(RootElement):
    def __init__(self, tag):
        super(CallableElement, self).__init__(tag)
        self.name = tag.attrib["name"]
