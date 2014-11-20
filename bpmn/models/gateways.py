from ..core import StringAttribute
from .common import FlowNode

class Gateway(FlowNode):
    gatewayDirection = StringAttribute('gatewayDirection', 'Unspecified')


class ParallelGateway(Gateway):
    pass
    

class ExclusiveGateway(Gateway):
    pass
