import warnings


class MetaRegister(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_cls = super(MetaRegister, cls).__new__(cls, name, bases, attrs)
        cls.registry[name] = new_cls
        return new_cls

def analyze_node(node):
    tagname = node.tag[0].upper() + node.tag[1:]
    try:
        tagclass = MetaRegister.registry[tagname]
    except KeyError:
        warnings.warn('{0} is not implemented'.format(tagname))
        return
    return tagclass(node)
