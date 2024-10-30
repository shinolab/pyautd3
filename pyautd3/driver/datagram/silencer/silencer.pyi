from datetime import timedelta
from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import builder
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.silencer.fixed_completion_time import FixedCompletionTime
from pyautd3.driver.datagram.silencer.fixed_update_rate import FixedUpdateRate
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTM
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import SilencerTarget
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold

T = TypeVar("T", FixedCompletionTime, FixedUpdateRate)

class Silencer(Datagram, Generic[T]):
    _inner: T
    _strict_mode: bool
    def __init__(self, config: T | None = None) -> None: ...
    def with_strict_mode(self, mode: bool) -> Self: ...
    def is_valid(self, target: ModulationBase | FociSTM | GainSTM) -> bool: ...
    def _datagram_ptr(self, _: Geometry) -> DatagramPtr: ...
    def with_target(self, target: SilencerTarget) -> Silencer: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Silencer]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Silencer]: ...
    @staticmethod
    def disable() -> Silencer[FixedCompletionTime]: ...
    @property
    def target(self) -> SilencerTarget: ...
