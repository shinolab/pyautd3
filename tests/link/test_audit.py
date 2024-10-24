from pyautd3 import AUTD3, Controller
from pyautd3.link.audit import Audit


def test_audit():
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder()) as _:
        pass
