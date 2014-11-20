from .common import FlowNode

class Gateway(FlowNode):
    def __init__(self, tag):
        super(Gateway, self).__init__(tag)
        self.gatewayDirection = tag.attrib.get("gatewayDirection", "Unspecified")


class ParallelGateway(Gateway):
    def __init__(self, tag):
        super(ParallelGateway, self).__init__(tag)
    

class ExclusiveGateway(Gateway):
    def __init__(self, tag):
        super(ExclusiveGateway, self).__init__(tag)
