import platform
from typing import Self

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import SleeperTag, SleeperWrap
from pyautd3.native_methods.autd3capi_driver import SpinStrategyTag as SpinStrategy
from pyautd3.utils import Duration


class StdSleeper:
    timer_resolution: int | None

    def __init__(self: Self, *, timer_resolution: int | None = 1) -> None:
        self.timer_resolution = timer_resolution

    def _inner(self: Self) -> SleeperWrap:
        return SleeperWrap(SleeperTag.Std, self.timer_resolution or 0)


class SpinSleeper:
    native_accuracy: Duration
    spin_strategy: SpinStrategy

    def __init__(
        self: Self,
        native_accuracy: Duration | None = None,
    ) -> None:
        self.native_accuracy = native_accuracy or Duration.from_nanos(int(Base().spin_sleep_default_accuracy()))
        self.spin_strategy = SpinStrategy.SpinLoopHint if platform.system() == "Windows" else SpinStrategy.YieldThread

    def with_spin_strategy(self: Self, spin_strategy: SpinStrategy) -> Self:
        self.spin_strategy = spin_strategy
        return self

    def _inner(self: Self) -> SleeperWrap:
        return SleeperWrap(SleeperTag.Spin, self.native_accuracy.as_nanos(), self.spin_strategy)


class WaitableSleeper:
    def __init__(self: Self) -> None:
        pass

    def _inner(self: Self) -> SleeperWrap:
        if platform.system() != "Windows":  # pragma: no cover
            err = "WaitableSleeper is only supported on Windows"  # pragma: no cover
            raise RuntimeError(err)  # pragma: no cover
        return SleeperWrap(SleeperTag.Waitable, 0)  # pragma: no cover
