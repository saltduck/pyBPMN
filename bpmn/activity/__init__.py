from bpmn.common import FlowNode


class Activity(FlowNode):
    def __init__(self, tag):
        super(Activity,self).__init__(tag)
        self.isForCompensation = tag.attrib.get("isForCompensation", False)
        self.startQuantity = tag.attrib.get("startQuantity", 1)
        self.completionQuantity = tag.attrib.get("completionQuantity", 1)

    @property
    def auto_instantiate(self):
        """ If the Activity does not have an incoming Sequence Flow,
        then the Activity MUST be instantiated when the Process is instantiated.
        There are two exceptions to this: Compensation Activities and Event Sub-Processes.
        """
        return len(self.incoming) == 0

    def instantiate(self):
        return ActivityInst(self)


class ActivityInst(object):
    def __init__(self, activity):
        self.activity = activity
        self.state = "ready"

    def wait_for_complete(self, *args, **kwargs):
        return self.activity.wait_for_complete(*args, **kwargs)

    def get_next(self, *args, **kwargs):
        return self.activity.get_next(*args, **kwargs)

class CompensationActivity(Activity):
    auto_instantiate = False


class EventSubProcesse(Activity):
    auto_instantiate = False
