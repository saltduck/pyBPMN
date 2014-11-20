from .activities import Task


class UserTask(Task):
    def __init__(self, tag):
        super(UserTask,self).__init__(tag)
        self.implementation = tag.attrib.get("implementation", "##unspecified")


class PotentialOwner():pass
