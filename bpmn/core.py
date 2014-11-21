from .exceptions import XMLFormatError


class BaseAttribute(object):
    def __init__(self, xmlattr, default=None, required=False):
        self.xmlattr = xmlattr
        self.required = required
        self.default = default

    def getvalue(self, element):
        if self.required:
            return element.tag.attrib[self.xmlattr]
        default = self.default
        if callable(default):
            default = default()
        return element.tag.attrib.get(self.xmlattr, default)

class StringAttribute(BaseAttribute):
    def __init__(self, xmlattr, default='', required=False):
        super(StringAttribute, self).__init__(xmlattr, default, required)


class UriAttribute(StringAttribute):
    def getvalue(self, element):
        def isuri(value):
            # TODO
            return True
        value = super(UriAttribute, self).getvalue(element)
        if value and not isuri(value):
            raise XMLFormatError('{0} must be a valid URI'.format(self.xmlstr))
        return value


class BooleanAttribute(BaseAttribute):
    def __init__(self, xmlattr, default=False, required=False):
        super(BooleanAttribute, self).__init__(xmlattr, default, required)

    def getvalue(self, element):
        value = super(BooleanAttribute, self).getvalue(element)
        if isinstance(value, (str, unicode)):
            value = value.lower() in ('true', 'yes')
        return value


class IntAttribute(BaseAttribute):
    def __init__(self, xmlattr, default=0, required=False):
        super(IntAttribute, self).__init__(xmlattr, default, required)

    def getvalue(self, element):
        value = super(IntAttribute, self).getvalue(element)
        return int(value)


class MultiAssociation(BaseAttribute):
    def __init__(self, targetclass, required=False):
        self.targetclass = targetclass
        self.required = required

    def getvalue(self, element):
        if isinstance(self.targetclass, (str, unicode)):
            self.targetclass = MetaRegister.registry[self.targetclass]
        return [e for e in element.children.values() if isinstance(e, self.targetclass)]


class SingleAssociation(MultiAssociation):
    def getvalue(self, element):
        values = super(SingleAssociation, self).getvalue(element)
        if len(values) > 1:
            raise XMLFormatError('There should be only 1 association to {0} in {1}(id={2})'.format(attribute, self.tagname, self.id))
        if len(values) == 0:
            value = None
        else:   # len(values) == 1
            value = values[0]
        return value
    

class XMLTagText(BaseAttribute):
    def __init__(self):
        pass

    def getvalue(self, element):
        return element.tag.text


class MetaRegister(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_cls = super(MetaRegister, cls).__new__(cls, name, bases, attrs)
        new_cls.attributes = {}
        for base in bases:
            if hasattr(base, 'attributes'):
                new_cls.attributes.update(base.attributes)
        for attrname, attr in attrs.items():
            if isinstance(attr, BaseAttribute):
                new_cls.attributes[attrname] = attr
        cls.registry[name] = new_cls
        return new_cls
