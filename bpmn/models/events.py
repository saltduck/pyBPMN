from ..core import StringAttribute, BooleanAttribute
from .common import FlowNode


class Event(FlowNode):
    def trigger(self):
        raise NotImplementedError


class ThrowEvent(Event):
    inputSet = StringAttribute('inputSet')


class CatchEvent(Event):
    parallelMultiple = BooleanAttribute('parallelMultiple')
    outputSet = StringAttribute('outputSet')


class StartEvent(CatchEvent):
    auto_instantiate = True
    isInterrupting = BooleanAttribute('isInterrupting')

    def trigger(self):
        self.container.instantiate()


class EndEvent(ThrowEvent):
    def __init__(self, tag):
        super(EndEvent,self).__init__(tag)
