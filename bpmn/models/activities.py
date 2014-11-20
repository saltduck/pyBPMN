from gettext import gettext as _

from bpmn.exceptions import XMLFormatError
from .common import FlowNode


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


class Task(Activity):
    def __init__(self, tag):
        super(Task,self).__init__(tag)
        

class ScriptTask(Task):
    SCRIPTFORMAT = "application/x-pybpmn"
    
    def __init__(self, tag):
        super(ScriptTask,self).__init__(tag)
        self.script = tag.attrib.get("script")
        self.scriptFormat = tag.attrib.get("scriptFormat")
        if self.script:
            if not self.scriptFormat:
                raise XMLFormatError(_("ScriptTask must have scriptFormat attribute if script attribute exists."))
            if self.scriptFormat <> self.SCRIPTFORMAT:
                raise XMLFormatError(_("ScriptTask support only application/x-pybpmn language."))
        
    def wait_for_complete(self):
        super(ScriptTask, self).wait_for_complete()
        if not self.script:
            return
        if self.scriptFormat == self.SCRIPTFORMAT:
            exec(self.script)


class ServiceTask(Task):
    def __init__(self, tag):
        super(ServiceTask,self).__init__(tag)
        self.implementation = tag.attrib.get("implementation", "##WebService")
