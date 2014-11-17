from nose.tools import eq_, assert_raises
from xml.etree import ElementTree

from bpmn import XMLFormatError
from .scripttask import ScriptTask

def test_scripttask():
    tag = ElementTree.fromstring("""<scriptTask id="1"></scriptTask>""")
    task = ScriptTask(tag)
    task.wait_for_complete()

    tag = ElementTree.fromstring("""<scriptTask id="1" script="aaa"></scriptTask>""")
    with assert_raises(XMLFormatError):
        task = ScriptTask(tag)
