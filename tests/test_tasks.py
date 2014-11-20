from nose.tools import eq_

from bpmn import engine
from bpmn.models.common import FormalExpression
from bpmn.models.activities import ResourceParameterBinding
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
<resourceRef>regionalManager</resourceRef>
<resourceParameterBinding parameterRef="buyerName">
<formalExpression>getDataInput('order')/address/name</formalExpression>
</resourceParameterBinding>
<resourceParameterBinding parameterRef="region">
<formalExpression>getDataInput('order')/address/country</formalExpression>
</resourceParameterBinding>
</potentialOwner>
</userTask>
</definitions>
    """
    engine.load_definition(xmlstr)
    eq_(engine.db.count(), 10)
    usertask = engine.db['ApproveOrder']
    eq_(usertask.name, 'ApproveOrder')
    eq_(len(usertask.resources), 1)
    po = usertask.resources[0]
    assert isinstance(po, PotentialOwner)
    eq_(po.resourceRef.refid, 'regionalManager')
    eq_(po.resource.name, 'Regional Manager')
    eq_(len(po.resourceParameterBindings), 2)
    po.resourceParameterBindings.sort()
    para1, para2 = po.resourceParameterBindings
    assert isinstance(para1, ResourceParameterBinding)
    assert isinstance(para2, ResourceParameterBinding)
    eq_(para1.parameterRef, 'buyerName')
    eq_(para1.parameter.name, 'Buyer Name')
    eq_(para2.parameterRef, 'region')
    eq_(para2.parameter.name, 'Region')
    assert isinstance(para1.expression, FormalExpression)
    assert isinstance(para2.expression, FormalExpression)
    eq_(para1.expression.body, "getDataInput('order')/address/name")
    eq_(para2.expression.body, "getDataInput('order')/address/country")

    
