import platform
from typing import Self

from pyautd3.derive import builder
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import SpinStrategyTag as SpinStrategy
from pyautd3.native_methods.autd3capi_driver import TimerStrategyWrap
from pyautd3.native_methods.utils import ConstantADT


@builder
class StdSleeper:
    _prop_timer_resolution: int | None

    def __init__(self: Self, *, timer_resolution: int | None = 1) -> None:
        self._prop_timer_resolution = timer_resolution


@builder
class SpinSleeper:
    _prop_native_accuracy_ns: int
    _param_spin_strategy: SpinStrategy

    def __init__(
        self: Self,
        native_accuracy_ns: int | None = None,
    ) -> None:
        self._prop_native_accuracy_ns = native_accuracy_ns if native_accuracy_ns is not None else int(Base().timer_strategy_spin_default_accuracy())
        self._param_spin_strategy = SpinStrategy.SpinLoopHint if platform.system() == "Windows" else SpinStrategy.YieldThread


@builder
class AsyncSleeper:
    _prop_timer_resolution: int | None

    def __init__(self: Self, *, timer_resolution: int | None = 1) -> None:
        self._prop_timer_resolution = timer_resolution


class WaitableSleeper:
    def __init__(self: Self) -> None:
        pass


class TimerStrategy(metaclass=ConstantADT):
    @staticmethod
    def Std(sleeper: StdSleeper) -> TimerStrategyWrap:  # noqa: N802
        return Base().timer_strategy_std(sleeper._prop_timer_resolution if sleeper._prop_timer_resolution is not None else 0)

    @staticmethod
    def Spin(sleeper: SpinSleeper) -> TimerStrategyWrap:  # noqa: N802
        return Base().timer_strategy_spin(sleeper._prop_native_accuracy_ns, sleeper._param_spin_strategy)

    @staticmethod
    def Async(sleeper: AsyncSleeper) -> TimerStrategyWrap:  # noqa: N802
        return Base().timer_strategy_async(sleeper.timer_resolution if sleeper.timer_resolution is not None else 0)

    @staticmethod
    def Waitable(_sleeper: WaitableSleeper) -> TimerStrategyWrap:  # noqa: N802
        return Base().timer_strategy_waitable()

    def __new__(cls: type["TimerStrategy"]) -> "TimerStrategy":
        raise NotImplementedError
