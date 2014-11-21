from nose.tools import raises
from bpmn import engine

def test_no_default():
    engine.load_definition("""
<definitions targetNamespace="http://www.example.org/UserTaskExample" xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <process id="p1" name="Process1">
        <task id="1"></task>
        <sequenceFlow sourceRef="1" targetRef="2"></sequenceFlow>
        <exclusiveGateway id="2">
        </exclusiveGateway>
        <sequenceFlow id="sf_2" sourceRef="2" targetRef="3"></sequenceFlow>
        <task id="3"></task>
        <sequenceFlow id="sf_3" sourceRef="2" targetRef="4"></sequenceFlow>
        <sequenceFlow sourceRef="3" targetRef="end"></sequenceFlow>
        <task id="4"></task>
        <sequenceFlow sourceRef="4" targetRef="end"></sequenceFlow>
        <endEvent id="end"></endEvent>
    </process>
</definitions>""")
    process = engine.processes['p1']
    process.instantiate()
    process.join()

def test_default1():
    engine.load_definition("""
<definitions targetNamespace="http://www.example.org/UserTaskExample" xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <process id="p1" name="Process1">
        <task id="1"></task>
        <sequenceFlow sourceRef="1" targetRef="2"></sequenceFlow>
        <exclusiveGateway id="2" default="sf_2">
        </exclusiveGateway>
        <sequenceFlow id="sf_2" sourceRef="2" targetRef="3"></sequenceFlow>
        <task id="3"></task>
        <sequenceFlow id="sf_3" sourceRef="2" targetRef="4"></sequenceFlow>
        <sequenceFlow sourceRef="3" targetRef="end"></sequenceFlow>
        <task id="4"></task>
        <sequenceFlow sourceRef="4" targetRef="end"></sequenceFlow>
        <endEvent id="end"></endEvent>
    </process>
</definitions>""")
    process = engine.processes['p1']
    process.instantiate()
    process.join()

def test_default2():
    engine.load_definition("""
<definitions targetNamespace="http://www.example.org/UserTaskExample" xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <process id="p1" name="Process1">
        <task id="1"></task>
        <sequenceFlow sourceRef="1" targetRef="2"></sequenceFlow>
        <exclusiveGateway id="2" default="sf_3">
        </exclusiveGateway>
        <sequenceFlow id="sf_2" sourceRef="2" targetRef="3"></sequenceFlow>
        <task id="3"></task>
        <sequenceFlow id="sf_3" sourceRef="2" targetRef="4"></sequenceFlow>
        <sequenceFlow sourceRef="3" targetRef="end"></sequenceFlow>
        <task id="4"></task>
        <sequenceFlow sourceRef="4" targetRef="end"></sequenceFlow>
        <endEvent id="end"></endEvent>
    </process>
</definitions>""")
    process = engine.processes['p1']
    process.instantiate()
    process.join()
