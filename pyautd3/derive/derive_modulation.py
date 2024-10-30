from collections.abc import Iterable


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

    cls.with_cache = with_cache  # type: ignore[attr-defined]
    cls.with_fir = with_fir  # type: ignore[attr-defined]
    cls.with_radiation_pressure = with_radiation_pressure  # type: ignore[attr-defined]

    return cls
