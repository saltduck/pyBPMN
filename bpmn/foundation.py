

class RootElement(object):
    def __init__(self, tag):
        super(RootElement, self).__init__()


class BaseElement(RootElement):
    def __init__(self, tag):
        super(BaseElement, self).__init__(tag)
        self.id = tag.attrib["id"]


class Documentation(BaseElement):
    def __init__(self, tag):
        super(Documentation, self).__init__(tag)
        self.text = tag.attrib.get["text"]
        self.textFormat = tag.attrib.get["textFormat"]
