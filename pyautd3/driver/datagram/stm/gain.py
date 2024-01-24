import ctypes
from collections.abc import Iterable
from datetime import timedelta

import numpy as np

from pyautd3.driver.common.sampling_config import SamplingConfiguration
from pyautd3.driver.geometry import Geometry
from pyautd3.gain.gain import IGain
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import (
    DatagramPtr,
    GainPtr,
    GainSTMMode,
)
from pyautd3.native_methods.utils import _validate_ptr

from .stm import _STM


class GainSTM(_STM):
    """GainSTM is an STM for moving any Gain."""

    _gains: list[IGain]
    _mode: GainSTMMode

    def __init__(
        self: "GainSTM",
        *,
        freq: float | None = None,
        period: timedelta | None = None,
        sampling_config: SamplingConfiguration | None = None,
    ) -> None:
        """Constructor.

        Arguments:
        ---------
            freq: Frequency of STM [Hz]. The frequency closest to `freq` from the possible frequencies is set.
            period: only for internal use.
            sampling_config: only for internal use.
        """
        super().__init__(freq, period, sampling_config)
        self._gains = []
        self._mode = GainSTMMode.PhaseIntensityFull

    def _datagram_ptr(self: "GainSTM", geometry: Geometry) -> DatagramPtr:
        gains: np.ndarray = np.ndarray(len(self._gains), dtype=GainPtr)
        for i, g in enumerate(self._gains):
            gains[i]["_0"] = g._gain_ptr(geometry)._0
        return _validate_ptr(
            Base().stm_gain(
                self._props(),
                gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
                len(self._gains),
                self._mode,
            ),
        )

    @staticmethod
    def from_freq(freq: float) -> "GainSTM":
        """Constructor.

        Arguments:
        ---------
            freq: freq
        """
        return GainSTM(freq=freq)

    @staticmethod
    def from_sampling_config(config: SamplingConfiguration) -> "GainSTM":
        """Constructor.

        Arguments:
        ---------
            config: Sampling configuration
        """
        return GainSTM(sampling_config=config)

    @staticmethod
    def from_period(period: timedelta) -> "GainSTM":
        """Constructor.

        Arguments:
        ---------
            period: Period.
        """
        return GainSTM(period=period)

    def add_gain(self: "GainSTM", gain: IGain) -> "GainSTM":
        """Add gain.

        Arguments:
        ---------
            gain: Gain
        """
        self._gains.append(gain)
        return self

    def add_gains_from_iter(self: "GainSTM", iterable: Iterable[IGain]) -> "GainSTM":
        """Add gains.

        Arguments:
        ---------
            iterable: Iterable of gains
        """
        self._gains.extend(iterable)
        return self

    @property
    def frequency(self: "GainSTM") -> float:
        """Frequency [Hz]."""
        return self._frequency_from_size(len(self._gains))

    @property
    def period(self: "GainSTM") -> timedelta:
        """Period."""
        return self._period_from_size(len(self._gains))

    @property
    def sampling_config(self: "GainSTM") -> SamplingConfiguration:
        """Sampling configuration."""
        return self._sampling_config_from_size(len(self._gains))

    def with_mode(self: "GainSTM", mode: GainSTMMode) -> "GainSTM":
        """Set GainSTMMode.

        Arguments:
        ---------
            mode: GainSTMMode
        """
        self._mode = mode
        return self

    def with_start_idx(self: "GainSTM", value: int | None) -> "GainSTM":
        """Set the start index of STM.

        Arguments:
        ---------
            value: Start index of STM.
        """
        self._start_idx = -1 if value is None else value
        return self

    def with_finish_idx(self: "GainSTM", value: int | None) -> "GainSTM":
        """Set the finish index of STM.

        Arguments:
        ---------
            value: Finish index of STM.
        """
        self._finish_idx = -1 if value is None else value
        return self
