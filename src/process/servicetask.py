from task import Task


class ServiceTask(Task):
    def __init__(self, tag):
        super(ServiceTask,self).__init__(tag)
        self.implementation = tag.attrib.get("implementation", "##WebService")