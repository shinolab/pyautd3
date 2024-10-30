from collections.abc import Iterable
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap


def modulation(cls):
    def with_cache(self):
        from pyautd3.modulation.cache import Cache

        return Cache(self)

    def with_fir(self, iterable: Iterable[float]):
        from pyautd3.modulation.fir import Fir

        return Fir(self, iterable)

    def with_radiation_pressure(self):
        from pyautd3.modulation.radiation_pressure import RadiationPressure

        return RadiationPressure(self)

    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None):
        from pyautd3.driver.datagram.with_segment import DatagramWithSegment

        return DatagramWithSegment(self, segment, transition_mode)

    cls.with_cache = with_cache  # type: ignore[attr-defined]
    cls.with_fir = with_fir  # type: ignore[attr-defined]
    cls.with_radiation_pressure = with_radiation_pressure  # type: ignore[attr-defined]
    cls.with_segment = with_segment  # type: ignore[attr-defined]

    return cls
