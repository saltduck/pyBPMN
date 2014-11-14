from nose.tools import eq_

from bpmn.process import ProcessDef

def test_1():
    pd = ProcessDef("""
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <bpmn:process id="p1" name="process1">
        <startEvent id="1" name="START"></startEvent>
        <scriptTask id="2" scriptFormat="application/x-pybpmn">
            <script>print "Hello, World"</script>
        </scriptTask>
        <sequenceFlow sourceRef="1" targetRef="2"></sequenceFlow>
        <endEvent id="3"></endEvent>
        <sequenceFlow sourceRef="2" targetRef="3"></sequenceFlow>
    </bpmn:process>
</bpmn:definitions>""")
    proc1 = pd.new()
    eq_(len(proc1.objects), 3, str(proc1.objects))
    eq_(len(proc1.tokens), 1)
    proc1.start()
    assert not proc1.tokens
