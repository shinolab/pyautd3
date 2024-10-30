from typing import Self

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTM
from pyautd3.driver.utils import _validate_nonzero_u16
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, SilencerTarget


class FixedUpdateRate:
    intensity: int
    phase: int

    def __init__(self: Self, *, intensity: int, phase: int) -> None:
        self.intensity = _validate_nonzero_u16(intensity)
        self.phase = _validate_nonzero_u16(phase)

    def _is_valid(self: Self, v: Modulation | FociSTM | GainSTM, _strict_mode: bool) -> bool:  # noqa: FBT001
        return bool(
            Base().datagram_silencer_fixed_update_rate_is_valid(
                self.intensity,
                self.phase,
                v._sampling_config_intensity()._inner,
                v._sampling_config_phase()._inner,
            ),
        )

    def _datagram_ptr(self: Self, _strict_mode: bool, target: SilencerTarget) -> DatagramPtr:  # noqa: FBT001
        return Base().datagram_silencer_from_update_rate(
            self.intensity,
            self.phase,
            target,
        )
