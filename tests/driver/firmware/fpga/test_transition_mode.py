import pytest

from pyautd3 import TransitionMode
from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.native_methods.autd3capi_driver import GPIOIn, TransitionModeTag


def test_transition_mode_sync_idx():
    mode = TransitionMode.SyncIdx
    assert mode.tag == TransitionModeTag.SyncIdx
    assert mode.value == 0


def test_transition_mode_sys_time():
    sys_time = DcSysTime.now()
    mode = TransitionMode.SysTime(sys_time)
    assert mode.tag == TransitionModeTag.SysTime
    assert mode.value == sys_time.sys_time


def test_transition_mode_gpio():
    mode = TransitionMode.GPIO(GPIOIn.I1)
    assert mode.tag == TransitionModeTag.Gpio
    assert mode.value == 1


def test_transition_mode_ext():
    mode = TransitionMode.Ext
    assert mode.tag == TransitionModeTag.Ext
    assert mode.value == 0


def test_transition_mode_immediate():
    mode = TransitionMode.Immediate
    assert mode.tag == TransitionModeTag.Immediate
    assert mode.value == 0


def test_transition_mode_ctor():
    with pytest.raises(NotImplementedError):
        _ = TransitionMode()
