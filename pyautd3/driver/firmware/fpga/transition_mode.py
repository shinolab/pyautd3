from abc import ABCMeta, abstractmethod
from typing import Self

from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.native_methods.autd3 import GPIOIn
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import TransitionModeWrap


class TransitionMode(metaclass=ABCMeta):
    @abstractmethod
    def _inner(self: Self) -> TransitionModeWrap:
        pass


class InfiniteTransitionMode(TransitionMode):
    pass


class FiniteTransitionMode(TransitionMode):
    pass


class Immediate(InfiniteTransitionMode, TransitionMode):
    def __init__(self: Self) -> None:
        pass

    def _inner(self: Self) -> TransitionModeWrap:
        return Base().transition_mode_immediate()


class Ext(InfiniteTransitionMode, TransitionMode):
    def __init__(self: Self) -> None:
        pass

    def _inner(self: Self) -> TransitionModeWrap:
        return Base().transition_mode_ext()


class SyncIdx(FiniteTransitionMode, TransitionMode):
    def __init__(self: Self) -> None:
        pass

    def _inner(self: Self) -> TransitionModeWrap:
        return Base().transition_mode_sync_idx()


class SysTime(FiniteTransitionMode, TransitionMode):
    def __init__(self: Self, sys_time: DcSysTime) -> None:
        self._sys_time = sys_time

    def _inner(self: Self) -> TransitionModeWrap:
        return Base().transition_mode_sys_time(self._sys_time._inner)


class GPIO(FiniteTransitionMode, TransitionMode):
    def __init__(self: Self, gpio: GPIOIn) -> None:
        self._gpio = gpio

    def _inner(self: Self) -> TransitionModeWrap:
        return Base().transition_mode_gpio(self._gpio)


class Later(FiniteTransitionMode, InfiniteTransitionMode, TransitionMode):
    def __init__(self: Self) -> None:
        pass

    def _inner(self: Self) -> TransitionModeWrap:
        return Base().transition_mode_later()
