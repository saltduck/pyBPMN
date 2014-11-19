import uuid

from bpmn import engine


class BaseElement(object):
    def __init__(self, tag):
        super(BaseElement, self).__init__()
        self.id = tag.attrib.get("id", uuid.uuid1().hex)
        engine.db[self.id] = self


class RootElement(BaseElement):
    def __init__(self, tag):
        super(RootElement, self).__init__(tag)


class Documentation(BaseElement):
    def __init__(self, tag):
        super(Documentation, self).__init__(tag)
        self.text = tag.attrib.get["text"]
        self.textFormat = tag.attrib.get["textFormat"]
