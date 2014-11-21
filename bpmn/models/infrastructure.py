from ..core import StringAttribute, UriAttribute, MultiAssociation
from .foundation import XMLBaseElement


class Definitions(XMLBaseElement):
    id = StringAttribute('id')
    targetNamespace = StringAttribute('targetNamespace', required=True)
    expressionLanguage = UriAttribute('expressionLanguage', default='http://www.w3.org/1999/XPath')
    typeLanguage = UriAttribute('typeLanguage', default='http://www.w3.org/2001/XMLSchema')
    exporter = StringAttribute('exporter')
    exporterVersion = StringAttribute('exporterVersion')
    rootElements = MultiAssociation('RootElement')
    # diagrams = MultiAssociation('BPMNDiagram')
    imports = MultiAssociation('Import')
    extensions = MultiAssociation('Extension')
    relationships = MultiAssociation('Relationship')


class Import(XMLBaseElement):
    namespace = StringAttribute('namespace', required=True)
    importType = UriAttribute('importType', required=True)
    location = StringAttribute('location')
