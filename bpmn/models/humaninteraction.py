from ..core import StringAttribute
from .activities import Task
from .process import Performer


class UserTask(Task):
    implementation = StringAttribute('implementation', '##unspecified')


class HumanPerformer(Performer):
    pass


class PotentialOwner(HumanPerformer):
    pass
