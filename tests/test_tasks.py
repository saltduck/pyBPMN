from nose.tools import eq_

from bpmn import engine
from bpmn.models.common import FormalExpression
from bpmn.models.humaninteraction import PotentialOwner

def test_usertask():
    engine.db.clear()
    xmlstr = """
<definitions>
<resource id="regionalManager" name="Regional Manager">
<resourceParameter id="buyerName" isRequired="true" name="Buyer Name" type="xsd:string"/>
<resourceParameter id="region" isRequired="false" name="Region" type="xsd:string"/>
</resource>
<userTask id="ApproveOrder" name="ApproveOrder">
<potentialOwner>
<resourceRef>tns:regionalManager</resourceRef>
<resourceParameterBinding parameterRef="tns:buyerName">
<formalExpression>getDataInput('order')/address/name</formalExpression>
</resourceParameterBinding>
<resourceParameterBinding parameterRef="tns:region">
<formalExpression>getDataInput('order')/address/country</formalExpression>
</resourceParameterBinding>
</potentialOwner>
</userTask>
</definitions>
    """
    engine.load_definition(xmlstr)
    print engine.db.data
    eq_(engine.db.count(), 7)
    usertask = engine.db['ApproveOrder']
    eq_(usertask.name, 'ApproveOrder')
    eq_(len(usertask.resources), 1)
    po = usertask.resources[0]
    assert isinstance(po, PotentialOwner)
    eq_(po.resourceRef.name, 'tns:regionalManager')
    eq_(len(po.resourceParameterBindings), 2)
    para1, para2 = po.resourceParameterBindings
    eq_(para1.name, 'tns:buyerName')
    eq_(para2.name, 'tns:region')
    assert isinstance(para1, FormalExpression)
    assert isinstance(para2, FormalExpression)
    eq_(para1.expresssion.body, "getDataInput('order')/address/name")
    eq_(para2.expresssion.body, "getDataInput('order')/address/country")

    
