from nose.tools import eq_, assert_raises
from xml.etree import ElementTree

from bpmn import load_definition, XMLFormatError

def test_1():
    processes = load_definition("""
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <bpmn:process id="p1" name="process1">
        <startEvent id="1" name="START"></startEvent>
        <sequenceFlow sourceRef="1" targetRef="2"></sequenceFlow>
        <scriptTask id="2" scriptFormat="application/x-pybpmn" script="from time import sleep;sleep(2)"></scriptTask>
        <sequenceFlow sourceRef="2" targetRef="3"></sequenceFlow>
        <endEvent id="3"></endEvent>
    </bpmn:process>
    <bpmn:process id="p2" name="process2">
        <startEvent id="1" name="START"></startEvent>
        <sequenceFlow sourceRef="1" targetRef="2"></sequenceFlow>
        <scriptTask id="2" scriptFormat="application/x-pybpmn" script="from time import sleep;sleep(3)"></scriptTask>
        <sequenceFlow sourceRef="2" targetRef="3"></sequenceFlow>
        <endEvent id="3"></endEvent>
    </bpmn:process>
</bpmn:definitions>""")
    eq_(len(processes), 2)
    proc1, proc2 = processes
    eq_(len(proc1.objects), 3, str(proc1.objects))
    eq_(len(proc1.tokens), 1)
    proc1.start()
    proc2.start()
    proc1.join()
    proc2.join()
    assert not proc1.tokens
    assert not proc2.tokens

def test_scripttask():
    from bpmn.activity.scripttask import ScriptTask
    tag = ElementTree.fromstring("""<scriptTask></scriptTask>""")
    task = ScriptTask(tag)
    task.wait_for_complete()

    tag = ElementTree.fromstring("""<scriptTask script="aaa"></scriptTask>""")
    with assert_raises(XMLFormatError):
        task = ScriptTask(tag)
