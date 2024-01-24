from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.common.phase import Phase
from pyautd3.driver.datagram.gain import IGain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import GainPtr


class Uniform(IGain):
    """Gain with uniform amplitude and phase."""

    _intensity: EmitIntensity
    _phase: Phase

    def __init__(self: "Uniform", intensity: int | EmitIntensity) -> None:
        """Constructor.

        Arguments:
        ---------
            intensity: Emission intensity
        """
        super().__init__()
        self._intensity = EmitIntensity._cast(intensity)
        self._phase = Phase(0)

    def intensity(self: "Uniform") -> EmitIntensity:
        """Get emission intensity."""
        return self._intensity

    def with_phase(self: "Uniform", phase: Phase) -> "Uniform":
        """Set phase.

        Arguments:
        ---------
            phase: Phase
        """
        self._phase = phase
        return self

    def phase(self: "Uniform") -> Phase:
        """Get phase."""
        return self._phase

    def _gain_ptr(self: "Uniform", _: Geometry) -> GainPtr:
        return Base().gain_uniform(self._intensity.value, self._phase.value)
