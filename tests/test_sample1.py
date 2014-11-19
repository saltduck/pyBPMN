from nose.tools import eq_

from bpmn import engine

def test_sample1():
    engine.load_definition_file('tests/sample1.xml')
    proc = engine.processes['BuyerProcess']
    assert proc.objects
    inst = proc.instantiate()
    eq_(len(inst.tokens), 1)
    proc.join()
    assert len(proc.instances)==0
