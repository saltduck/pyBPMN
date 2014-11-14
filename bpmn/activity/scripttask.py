from gettext import gettext as _

from bpmn import XMLFormatError
from .task import Task


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
        if not self.script:
            return
        if self.scriptFormat == self.SCRIPTFORMAT:
            exec(self.script)
