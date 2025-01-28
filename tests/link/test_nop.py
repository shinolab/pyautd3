from pyautd3 import AUTD3, Controller
from pyautd3.link.nop import Nop


def test_nop():
    with Controller.open([AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])], Nop.builder()) as autd:
        autd.close()
