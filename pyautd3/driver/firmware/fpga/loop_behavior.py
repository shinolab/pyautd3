from pyautd3.autd_error import CantBeZeroError
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior
from pyautd3.native_methods.utils import ConstantADT


class LoopBehavior(metaclass=ConstantADT):
    Infinite: _LoopBehavior = Base().loop_behavior_infinite()

    @staticmethod
    def Finite(v: int) -> _LoopBehavior:  # noqa: N802
        if v < 1:
            raise CantBeZeroError(v)
        return Base().loop_behavior_finite(v)

    Once: _LoopBehavior = Base().loop_behavior_once()

    def __new__(cls: type["LoopBehavior"]) -> "LoopBehavior":
        raise NotImplementedError
