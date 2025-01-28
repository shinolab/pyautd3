from pyautd3 import AUTD3, Controller
from pyautd3.link.audit import Audit


def test_audit():
    with Controller.open([AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])], Audit.builder()) as _:
        pass
