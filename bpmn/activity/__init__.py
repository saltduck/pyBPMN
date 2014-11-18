from bpmn.common import FlowNode


class Activity(FlowNode):
    def __init__(self, tag):
        super(Activity,self).__init__(tag)
        self.isForCompensation = tag.attrib.get("isForCompensation", False)
        self.startQuantity = tag.attrib.get("startQuantity", 1)
        self.completionQuantity = tag.attrib.get("completionQuantity", 1)
        self.state = "none"
