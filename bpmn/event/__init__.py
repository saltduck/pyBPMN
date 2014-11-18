from bpmn.common import FlowNode

class Event(FlowNode):
    def __init__(self, tag):
        super(Event,self).__init__(tag)

    def trigger(self):
        raise NotImplementedError


class ThrowEvent(Event):
    def __init__(self, tag):
        super(ThrowEvent,self).__init__(tag)
        self.inputSet = tag.get("inputSet", None)


class CatchEvent(Event):
    def __init__(self, tag):
        super(CatchEvent,self).__init__(tag)
        self.parallelMultiple = tag.get("parallelMultiple", False)
        self.outputSet = tag.get("outputSet", None)
