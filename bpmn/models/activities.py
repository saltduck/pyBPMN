from gettext import gettext as _

from .. import engine
from bpmn.exceptions import XMLFormatError
from bpmn.core import StringAttribute, BooleanAttribute, IntAttribute, SingleAssociation, MultiAssociation
from .foundation import BaseElement
from .common import FlowNode, Expression, Resource, ResourceParameter


class Activity(FlowNode):
    isForCompensation = BooleanAttribute('isForCompensation', default=False)
    startQuantity = IntAttribute('startQuantity', default=1)
    completionQuantity = IntAttribute('completionQuantity', default=1)
    resources = MultiAssociation('ResourceRole')

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
    script = StringAttribute('script')
    scriptFormat = StringAttribute('scriptFormat')
    
    def validate(self):
        super(ScriptTask,self).validate()
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
    implementation = StringAttribute('implementation', default='##WebService')


class ResourceAssignmentExpression(BaseElement):
    expression = SingleAssociation(Expression, required=True)


class ResourceParameterBinding(BaseElement):
    parameterRef = StringAttribute('parameterRef', required=True)
    expression = SingleAssociation(Expression, required=True)

    @property
    def parameter(self):
        return engine.db[self.parameterRef]


class ResourceRole(BaseElement):
    name = StringAttribute('name')
    resourceRef = SingleAssociation('ResourceRef')
    resourceAssignmentExpression = SingleAssociation(ResourceAssignmentExpression)
    resourceParameterBindings = MultiAssociation(ResourceParameterBinding)

    def validate(self):
        if self.resourceRef and self.resourceAssignmentExpression:
            raise XMLFormatError('resourceRef and resourceAssignmentExpression should not exists together.')
        if self.resourceParameterBindings and not self.resourceRef:
            raise XMLFormatError('resourceParameterBindings is only applicable if a resourceRef is specified.')

    @property
    def resource(self):
        return engine.db[self.resourceRef.refid]
