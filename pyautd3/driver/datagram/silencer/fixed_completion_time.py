from typing import Self

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTM
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, SilencerTarget
from pyautd3.utils import Duration


class FixedCompletionTime:
    intensity: Duration
    phase: Duration

    def __init__(self: Self, *, intensity: Duration, phase: Duration) -> None:
        self.intensity = intensity
        self.phase = phase

    def _is_valid(
        self: Self,
        v: Modulation | FociSTM | GainSTM,
        strict_mode: bool,  # noqa: FBT001
    ) -> bool:
        return bool(
            Base().datagram_silencer_fixed_completion_time_is_valid(
                self.intensity._inner,
                self.phase._inner,
                strict_mode,
                v._sampling_config_intensity()._inner,
                v._sampling_config_phase()._inner,
            ),
        )

    def _datagram_ptr(self: Self, strict_mode: bool, target: SilencerTarget) -> DatagramPtr:  # noqa: FBT001
        return Base().datagram_silencer_from_completion_time(
            self.intensity._inner,
            self.phase._inner,
            strict_mode,
            target,
        )
