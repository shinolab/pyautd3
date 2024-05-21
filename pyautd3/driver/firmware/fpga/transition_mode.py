from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import TransitionModeWrap
from pyautd3.native_methods.utils import ConstantADT


class TransitionMode(metaclass=ConstantADT):
    SyncIdx: TransitionModeWrap = Base().transition_mode_sync_idx()

    Ext: TransitionModeWrap = Base().transition_mode_ext()
    Immediate: TransitionModeWrap = Base().transition_mode_immediate()

    def __new__(cls: type["TransitionMode"]) -> "TransitionMode":
        raise NotImplementedError
