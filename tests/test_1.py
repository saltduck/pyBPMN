from nose.tools import eq_, assert_raises, timed
from xml.etree import ElementTree

from bpmn import engine

@timed(3.5)
def test_1():
    engine.db.clear()
    engine.load_definition("""
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <process id="p1" name="process1">
        <startEvent id="event_1" name="START"></startEvent>
        <sequenceFlow id="sf1" sourceRef="event_1" targetRef="2"></sequenceFlow>
        <scriptTask id="2" scriptFormat="application/x-pybpmn" script="from time import sleep;sleep(2)"></scriptTask>
        <sequenceFlow id="sf2" sourceRef="2" targetRef="event_2"></sequenceFlow>
        <endEvent id="event_2"></endEvent>
    </process>
    <process id="p2" name="process2">
        <scriptTask id="2" scriptFormat="application/x-pybpmn" script="from time import sleep;sleep(3)"></scriptTask>
        <sequenceFlow id="sf2" sourceRef="2" targetRef="event_3"></sequenceFlow>
        <endEvent id="event_3"></endEvent>
    </process>
</bpmn:definitions>""")
    eq_(len(engine.processes), 2)
    proc1 = engine.processes['p1']
    proc2 = engine.processes['p2']
    eq_(len(proc1.children), 5, str(proc1.children))
    eq_(len(proc2.children), 3, str(proc1.children))
    proc1.instantiate()
    proc2.instantiate()
    eq_(len(proc1.instances), 1)
    eq_(len(proc2.instances), 1)
    print proc1.instances[0].tokens
    eq_(len(proc1.instances[0].tokens), 1)
    eq_(len(proc2.instances[0].tokens), 1)
    proc1.join()
    proc2.join()
    assert not proc1.instances
    assert not proc2.instances
