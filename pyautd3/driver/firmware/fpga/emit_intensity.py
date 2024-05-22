from ctypes import c_uint8


class EmitIntensity:
    _value: c_uint8

    def __init__(self: "EmitIntensity", intensity: int) -> None:
        if isinstance(intensity, float):
            raise TypeError
        self._value = c_uint8(intensity)

    @property
    def value(self: "EmitIntensity") -> int:
        return self._value.value

    @staticmethod
    def maximum() -> "EmitIntensity":
        return EmitIntensity(0xFF)

    @staticmethod
    def minimum() -> "EmitIntensity":
        return EmitIntensity(0x00)

    def __floordiv__(self: "EmitIntensity", other: int) -> "EmitIntensity":
        return EmitIntensity(self.value // other)

    def __eq__(self: "EmitIntensity", __value: object) -> bool:
        return isinstance(__value, EmitIntensity) and self.value == __value.value

    def __str__(self: "EmitIntensity") -> str:
        return f"EmitIntensity({self.value})"

    def __repr__(self: "EmitIntensity") -> str:
        return f"EmitIntensity({self.value})"
