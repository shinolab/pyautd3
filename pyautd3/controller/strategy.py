from typing import Self

from pyautd3.controller.sleeper import SpinSleeper, SpinWaitSleeper, StdSleeper
from pyautd3.native_methods.autd3capi_driver import TimerStrategyTag, TimerStrategyWrap


class FixedSchedule:
    _sleeper: StdSleeper | SpinSleeper | SpinWaitSleeper

    def __init__(self: Self, sleeper: StdSleeper | SpinSleeper | SpinWaitSleeper | None = None) -> None:
        if sleeper is None:
            sleeper = SpinSleeper()
        self._sleeper = sleeper

    def _inner(self: Self) -> TimerStrategyWrap:
        return TimerStrategyWrap(TimerStrategyTag.FixedSchedule, self._sleeper._inner())


class FixedDelay:
    _sleeper: StdSleeper | SpinSleeper | SpinWaitSleeper

    def __init__(self: Self, sleeper: StdSleeper | SpinSleeper | SpinWaitSleeper) -> None:
        self._sleeper = sleeper

    def _inner(self: Self) -> TimerStrategyWrap:
        return TimerStrategyWrap(TimerStrategyTag.FixedDelay, self._sleeper._inner())
