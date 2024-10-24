from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GPIOIn, TransitionModeWrap
from pyautd3.native_methods.utils import ConstantADT


class TransitionMode(metaclass=ConstantADT):
    SyncIdx: TransitionModeWrap = Base().transition_mode_sync_idx()

    @staticmethod
    def SysTime(sys_time: DcSysTime) -> TransitionModeWrap:  # noqa: N802
        return Base().transition_mode_sys_time(sys_time.sys_time)

    @staticmethod
    def GPIO(gpio: GPIOIn) -> TransitionModeWrap:  # noqa: N802
        return Base().transition_mode_gpio(gpio)

    Ext: TransitionModeWrap = Base().transition_mode_ext()
    Immediate: TransitionModeWrap = Base().transition_mode_immediate()

    def __new__(cls: type["TransitionMode"]) -> "TransitionMode":
        raise NotImplementedError

    NONE: TransitionModeWrap = Base().transition_mode_none()
