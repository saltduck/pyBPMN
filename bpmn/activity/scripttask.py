from gettext import gettext as _

from task import Task


class ScriptTask(Task):
    SCRIPTFORMAT = "application/x-pybpmn"
    
    def __init__(self, tag):
        super(ScriptTask,self).__init__(tag)
        self.scriptFormat = tag.attrib["scriptFormat"]
        script_tag = tag.find("script")
        self.script = script_tag.text
        if self.scriptFormat <> self.SCRIPTFORMAT:
            raise NotImplementedError(_("ScriptTask support only application/x-pybpmn language."))
        
    def wait_for_complete(self):
        if self.scriptFormat == self.SCRIPTFORMAT:
            exec(self.script)
