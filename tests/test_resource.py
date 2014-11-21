from nose.tools import eq_, ok_

from bpmn import engine

def test_1():
    engine.db.clear()
    xmlstr = """
<definitions targetNamespace="http://www.example.org/UserTaskExample">
<resource id="regionalManager" name="Regional Manager">
<resourceParameter id="buyerName" isRequired="true" name="Buyer Name" type="xsd:string"/>
<resourceParameter id="region" isRequired="false" name="Region" type="xsd:string"/>
</resource>
</definitions>"""
    engine.load_definition(xmlstr)
    eq_(engine.db.count(), 4)
    eq_(len(engine.db['regionalManager'].resourceParameters), 2)
    ok_(engine.db['buyerName'].isRequired)
    assert not engine.db['region'].isRequired

    
