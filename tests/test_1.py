from nose.tools import eq_, assert_raises, timed
from xml.etree import ElementTree

from bpmn import load_definition

@timed(3.5)
def test_1():
    processes = load_definition("""
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <bpmn:process id="p1" name="process1">
        <startEvent id="1" name="START"></startEvent>
        <sequenceFlow id="sf1" sourceRef="1" targetRef="2"></sequenceFlow>
        <scriptTask id="2" scriptFormat="application/x-pybpmn" script="from time import sleep;sleep(2)"></scriptTask>
        <sequenceFlow id="sf2" sourceRef="2" targetRef="3"></sequenceFlow>
        <endEvent id="3"></endEvent>
    </bpmn:process>
    <bpmn:process id="p2" name="process2">
        <scriptTask id="2" scriptFormat="application/x-pybpmn" script="from time import sleep;sleep(3)"></scriptTask>
        <sequenceFlow id="sf2" sourceRef="2" targetRef="3"></sequenceFlow>
        <endEvent id="3"></endEvent>
    </bpmn:process>
</bpmn:definitions>""")
    eq_(len(processes), 2)
    proc1, proc2 = processes
    eq_(len(proc1.objects), 5, str(proc1.objects))
    eq_(len(proc2.objects), 3, str(proc1.objects))
    proc1.start()
    proc2.start()
    eq_(len(proc1.instances), 1)
    eq_(len(proc2.instances), 1)
    eq_(len(proc1.instances[0].tokens), 1)
    eq_(len(proc2.instances[0].tokens), 1)
    proc1.join()
    proc2.join()
    assert not proc1.instances
    assert not proc2.instances
