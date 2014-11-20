import warnings
from .core import MetaRegister

def analyze_node(node):
    tagname = node.tag[0].upper() + node.tag[1:]
    try:
        tagclass = MetaRegister.registry[tagname]
    except KeyError:
        warnings.warn('{0} is not implemented'.format(tagname))
        return
    return tagclass(node)
