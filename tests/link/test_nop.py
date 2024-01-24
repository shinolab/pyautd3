from pyautd3 import AUTD3, Controller
from pyautd3.link.nop import Nop


def test_nop():
    with Controller.builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_with(Nop.builder()) as autd:
        autd.close()
