from pyautd3 import transition_mode
from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.native_methods.autd3 import GPIOIn
from pyautd3.native_methods.autd3capi_driver import TransitionModeTag


def test_transition_mode_sync_idx():
    mode = transition_mode.SyncIdx()._inner()
    assert mode.tag == TransitionModeTag.SyncIdx
    assert mode.value.null == 0


def test_transition_mode_sys_time():
    sys_time = DcSysTime(10)
    mode = transition_mode.SysTime(sys_time)._inner()
    assert mode.tag == TransitionModeTag.SysTime
    assert mode.value.sys_time.dc_sys_time == sys_time.sys_time()


def test_transition_mode_gpio():
    mode = transition_mode.GPIO(GPIOIn(1))._inner()
    assert mode.tag == TransitionModeTag.Gpio
    assert mode.value.gpio_in == 1


def test_transition_mode_ext():
    mode = transition_mode.Ext()._inner()
    assert mode.tag == TransitionModeTag.Ext
    assert mode.value.null == 0


def test_transition_mode_immediate():
    mode = transition_mode.Immediate()._inner()
    assert mode.tag == TransitionModeTag.Immediate
    assert mode.value.null == 0


def test_transition_mode_later():
    mode = transition_mode.Later()._inner()
    assert mode.tag == TransitionModeTag.Later
    assert mode.value.null == 0
