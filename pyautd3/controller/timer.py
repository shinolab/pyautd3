import platform
from typing import Self

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import SpinStrategyTag as SpinStrategy
from pyautd3.native_methods.autd3capi_driver import TimerStrategyWrap
from pyautd3.native_methods.utils import ConstantADT


class StdSleeper:
    _timer_resolution: int | None

    def __init__(self: Self, *, timer_resolution: int | None = 1) -> None:
        self._timer_resolution = timer_resolution


class SpinSleeper:
    native_accuracy_ns: int
    spin_strategy: SpinStrategy

    def __init__(
        self: Self,
        native_accuracy_ns: int | None = None,
    ) -> None:
        self.native_accuracy_ns = native_accuracy_ns if native_accuracy_ns is not None else int(Base().timer_strategy_spin_default_accuracy())
        self.spin_strategy = SpinStrategy.SpinLoopHint if platform.system() == "Windows" else SpinStrategy.YieldThread

    def with_spin_strategy(self: Self, spin_strategy: SpinStrategy) -> Self:
        self.spin_strategy = spin_strategy
        return self


class AsyncSleeper:
    timer_resolution: int | None

    def __init__(self: Self, *, timer_resolution: int | None = 1) -> None:
        self.timer_resolution = timer_resolution


class WaitableSleeper:
    def __init__(self: Self) -> None:
        pass


class TimerStrategy(metaclass=ConstantADT):
    @staticmethod
    def Std(sleeper: StdSleeper) -> TimerStrategyWrap:  # noqa: N802
        return Base().timer_strategy_std(sleeper._timer_resolution if sleeper._timer_resolution is not None else 0)

    @staticmethod
    def Spin(sleeper: SpinSleeper) -> TimerStrategyWrap:  # noqa: N802
        return Base().timer_strategy_spin(sleeper.native_accuracy_ns, sleeper.spin_strategy)

    @staticmethod
    def Async(sleeper: AsyncSleeper) -> TimerStrategyWrap:  # noqa: N802
        return Base().timer_strategy_async(sleeper.timer_resolution if sleeper.timer_resolution is not None else 0)

    @staticmethod
    def Waitable(_sleeper: WaitableSleeper) -> TimerStrategyWrap:  # noqa: N802
        return Base().timer_strategy_waitable()

    def __new__(cls: type["TimerStrategy"]) -> "TimerStrategy":
        raise NotImplementedError
