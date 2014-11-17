from bpmn.common import FlowNode

class Gateway(FlowNode):
    def __init__(self, tag):
        super(Gateway, self).__init__(tag)
        self.gatewayDirection = tag.attrib.get("gatewayDirection", "Unspecified")
