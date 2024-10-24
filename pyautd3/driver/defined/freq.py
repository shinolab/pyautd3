from typing import Generic, Self, TypeVar

T = TypeVar("T", int, float)


class Freq(Generic[T]):
    _freq: T

    def __new__(cls: type["Freq"]) -> "Freq":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["Freq[T]"], freq: T) -> "Freq[T]":
        ins = super().__new__(cls)
        ins._freq = freq
        return ins

    @property
    def hz(self: Self) -> T:
        return self._freq

    def __eq__(self: Self, value: object) -> bool:
        return isinstance(value, Freq) and self._freq == value._freq


class _UnitHz:
    def __new__(cls: type["_UnitHz"]) -> "_UnitHz":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["_UnitHz"]) -> "_UnitHz":
        return super().__new__(cls)

    def __rmul__(self: Self, other: T) -> "Freq[T]":
        return Freq.__private_new__(other)


class _UnitkHz:
    def __new__(cls: type["_UnitkHz"]) -> "_UnitkHz":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["_UnitkHz"]) -> "_UnitkHz":
        return super().__new__(cls)

    def __rmul__(self: Self, other: T) -> "Freq[T]":
        return Freq.__private_new__(other * 1000)


Hz: _UnitHz = _UnitHz.__private_new__()
kHz: _UnitkHz = _UnitkHz.__private_new__()  # noqa: N816
