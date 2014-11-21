from nose.tools import eq_

from bpmn import engine

def test_sample1():
    engine.db.clear()
    engine.load_definition_file('tests/sample1.xml')
    proc = engine.processes['BuyerProcess']
    assert proc.children
    inst = proc.instantiate()
    proc.join()
