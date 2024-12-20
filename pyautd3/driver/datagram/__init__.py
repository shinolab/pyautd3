from forbiddenfruit import curse  # type: ignore[import-untyped]

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.datagram_tuple import DatagramTuple
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.utils import Duration

from .clear import Clear
from .debug import DebugSettings, DebugType
from .force_fan import ForceFan
from .phase_corr import PhaseCorrection
from .pulse_width_encoder import PulseWidthEncoder
from .reads_fpga_state import ReadsFPGAState
from .segment import SwapSegment
from .silencer import FixedCompletionTime, FixedUpdateRate, Silencer
from .stm import FociSTM, GainSTM, GainSTMMode
from .synchronize import Synchronize

__all__ = [
    "Clear",
    "Datagram",
    "DebugSettings",
    "DebugType",
    "FixedCompletionTime",
    "FixedUpdateRate",
    "FociSTM",
    "ForceFan",
    "GainSTM",
    "GainSTMMode",
    "PhaseCorrection",
    "PulseWidthEncoder",
    "ReadsFPGAState",
    "Silencer",
    "SwapSegment",
    "Synchronize",
]


def __with_parallel_threshold(self: tuple[Datagram, Datagram], threshold: int) -> DatagramWithParallelThreshold[DatagramTuple]:
    return DatagramWithParallelThreshold(DatagramTuple(self), threshold)


curse(tuple, "with_parallel_threshold", __with_parallel_threshold)


def __with_timeout(self: tuple[Datagram, Datagram], timeout: Duration | None) -> DatagramWithTimeout[DatagramTuple]:
    return DatagramWithTimeout(DatagramTuple(self), timeout)


curse(tuple, "with_timeout", __with_timeout)
