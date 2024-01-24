from datetime import timedelta

from pyautd3.native_methods.autd3capi_def import NativeMethods as Def
from pyautd3.native_methods.autd3capi_def import SamplingConfiguration as _SamplingConfiguration
from pyautd3.native_methods.utils import _validate_sampling_config


class SamplingConfiguration:
    """Sampling configuration."""

    _internal: _SamplingConfiguration

    def __new__(cls: type["SamplingConfiguration"]) -> "SamplingConfiguration":
        """DO NOT USE THIS CONSTRUCTOR."""
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["SamplingConfiguration"], internal: _SamplingConfiguration) -> "SamplingConfiguration":
        ins = super().__new__(cls)
        ins._internal = internal
        return ins

    @staticmethod
    def from_frequency_division(value: int) -> "SamplingConfiguration":
        """Create by sampling frequency division."""
        return SamplingConfiguration.__private_new__(_validate_sampling_config(Def().sampling_config_from_frequency_division(value)))

    @staticmethod
    def from_frequency(f: float) -> "SamplingConfiguration":
        """Create by sampling frequency."""
        return SamplingConfiguration.__private_new__(_validate_sampling_config(Def().sampling_config_from_frequency(f)))

    @staticmethod
    def from_period(p: timedelta) -> "SamplingConfiguration":
        """Create by sampling period."""
        return SamplingConfiguration.__private_new__(
            _validate_sampling_config(
                Def().sampling_config_from_period(int(p.total_seconds() * 1000.0 * 1000.0 * 1000.0)),
            ),
        )

    @property
    def frequency_division(self: "SamplingConfiguration") -> int:
        """Frequency division."""
        return int(Def().sampling_config_frequency_division(self._internal))

    @property
    def frequency(self: "SamplingConfiguration") -> float:
        """Sampling frequency."""
        return float(Def().sampling_config_frequency(self._internal))

    @property
    def period(self: "SamplingConfiguration") -> timedelta:
        """Sampling period."""
        return timedelta(seconds=int(Def().sampling_config_period(self._internal)) / 1000.0 / 1000.0 / 1000.0)
