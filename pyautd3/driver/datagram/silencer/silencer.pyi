from datetime import timedelta
from typing import Generic, Self, TypeVar
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.silencer.fixed_completion_time import FixedCompletionTime
from pyautd3.driver.datagram.silencer.fixed_update_rate import FixedUpdateRate
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTM
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, SilencerTarget

T = TypeVar("T", FixedCompletionTime, FixedUpdateRate)

class Silencer(IntoDatagramWithTimeout[Silencer], IntoDatagramWithParallelThreshold[Silencer], Datagram, Generic[T]):
    _inner: T
    _strict_mode: bool
    def __init__(self, config: T | None = None) -> None: ...
    def with_strict_mode(self, mode: bool) -> Self: ...
    def is_valid(self, target: ModulationBase | FociSTM | GainSTM) -> bool: ...
    def _datagram_ptr(self, _: Geometry) -> DatagramPtr: ...
    def with_target(self, target: SilencerTarget) -> Silencer: ...
    @staticmethod
    def disable() -> Silencer[FixedCompletionTime]: ...
    @property
    def target(self) -> SilencerTarget: ...
