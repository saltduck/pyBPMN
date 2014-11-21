import logging
logger = logging.getLogger(__file__)
from bpmn import engine
from bpmn.core import XMLTagText, StringAttribute, BooleanAttribute, SingleAssociation, MultiAssociation
from .foundation import BaseElement, RootElement, ReferenceElement


class FlowElement(BaseElement):
    auto_instantiate = False
    name = StringAttribute('name', default='')

    def instantiate(self):
        return self


class SequenceFlow(FlowElement):
    source_id = StringAttribute('sourceRef', required=True)
    target_id = StringAttribute('targetRef', required=True)
    isImmediate = BooleanAttribute('isImmediate', default=False)

    def process_refs(self, objects):
        self.sourceRef = objects[self.source_id]
        self.targetRef = objects[self.target_id]
        assert isinstance(self.sourceRef, FlowNode)
        assert isinstance(self.targetRef, FlowNode)
        self.targetRef.incoming.append(self)
        self.sourceRef.outgoing.append(self)

    def condition_ok(self):
        return False


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
    

class Expression(BaseElement):
    pass


class FormalExpression(Expression):
    language = StringAttribute('language')
    evaluatesTypeRef = SingleAssociation('ItemDefinition')
    body = XMLTagText()


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
    name = StringAttribute('name', required=True)


class ResourceParameter(BaseElement):
    name = StringAttribute('name', required=True)
    isRequired = BooleanAttribute('isRequired', required=True)


class Resource(RootElement):
    name = StringAttribute('name', required=True)
    resourceParameters = MultiAssociation(ResourceParameter)


class ResourceRef(ReferenceElement):
    pass


class CallableElement(RootElement):
    name = StringAttribute('name', required=True)
