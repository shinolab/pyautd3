from typing import Self

from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo


class Amplitude:
    _value: float

    def __new__(cls: type["Amplitude"]) -> "Amplitude":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["Amplitude"], value: float) -> "Amplitude":
        ins = super().__new__(cls)
        ins._value = value
        return ins

    @staticmethod
    def new_pascal(value: float) -> "Amplitude":
        return Amplitude.__private_new__(value)

    @staticmethod
    def new_spl(value: float) -> "Amplitude":
        return Amplitude.__private_new__(float(GainHolo().gain_holo_spl_to_pascal(value)))

    @property
    def pascal(self: Self) -> float:
        return self._value

    @property
    def spl(self: Self) -> float:
        return float(GainHolo().gain_holo_pascal_to_spl(self._value))

    class _UnitPascal:
        def __new__(cls: type["Amplitude._UnitPascal"]) -> "Amplitude._UnitPascal":
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["Amplitude._UnitPascal"]) -> "Amplitude._UnitPascal":
            return super().__new__(cls)

        def __rmul__(self: Self, other: float) -> "Amplitude":
            return Amplitude.new_pascal(other)

    class _UnitSPL:
        def __new__(cls: type["Amplitude._UnitSPL"]) -> "Amplitude._UnitSPL":
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["Amplitude._UnitSPL"]) -> "Amplitude._UnitSPL":
            return super().__new__(cls)

        def __rmul__(self: Self, other: float) -> "Amplitude":
            return Amplitude.new_spl(other)


Pa: Amplitude._UnitPascal = Amplitude._UnitPascal.__private_new__()
dB: Amplitude._UnitSPL = Amplitude._UnitSPL.__private_new__()  # noqa: N816
