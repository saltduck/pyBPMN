from .. import engine
from ..core import StringAttribute
from .common import FlowNode

class Gateway(FlowNode):
    gatewayDirection = StringAttribute('gatewayDirection', 'Unspecified')
    

class ExclusiveGateway(Gateway):
    default = StringAttribute('default')

    def get_next(self):
        for flow in self.outgoing:
            if flow.condition_ok():
                return [flow.targetRef]
        if self.default:
            return [engine.db[self.default].targetRef]
        raise RuntimeError('No default path.')


class ParallelGateway(Gateway):
    pass
