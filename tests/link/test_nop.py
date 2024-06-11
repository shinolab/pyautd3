from pyautd3 import AUTD3, Controller
from pyautd3.link.nop import Nop


def test_nop():
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(Nop.builder()) as autd:
        autd.close()
