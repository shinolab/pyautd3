import ctypes

from pyautd3.native_methods.autd3capi_driver import Duration as _Duration
from pyautd3.native_methods.autd3capi_driver import OptionDuration


class Duration:
    _inner: _Duration

    def __new__(cls: type["Duration"]) -> "Duration":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["Duration"], inner: _Duration) -> "Duration":
        ins = super().__new__(cls)
        ins._inner = inner
        return ins

    @staticmethod
    def from_nanos(ns: int) -> "Duration":
        inner = _Duration()
        inner.nanos = ns
        return Duration.__private_new__(inner)

    @staticmethod
    def from_micros(us: int) -> "Duration":
        return Duration.from_nanos(us * 1000)

    @staticmethod
    def from_millis(ms: int) -> "Duration":
        return Duration.from_micros(ms * 1000)

    @staticmethod
    def from_secs(s: int) -> "Duration":
        return Duration.from_millis(s * 1000)

    def as_nanos(self) -> int:
        return int(self._inner.nanos)

    def as_micros(self) -> int:
        return self.as_nanos() // 1000

    def as_millis(self) -> int:
        return self.as_micros() // 1000

    def as_secs(self) -> int:
        return self.as_millis() // 1000

    def __add__(self: "Duration", other: "Duration") -> "Duration":
        return Duration.from_nanos(self.as_nanos() + other.as_nanos())

    def __sub__(self: "Duration", other: "Duration") -> "Duration":
        return Duration.from_nanos(self.as_nanos() - other.as_nanos())

    def __mul__(self: "Duration", other: int) -> "Duration":
        return Duration.from_nanos(self.as_nanos() * other)

    def __truediv__(self: "Duration", other: int) -> "Duration":
        return Duration.from_nanos(self.as_nanos() // other)

    def __floordiv__(self: "Duration", other: int) -> "Duration":
        return Duration.from_nanos(self.as_nanos() // other)

    def __mod__(self: "Duration", other: int) -> "Duration":
        return Duration.from_nanos(self.as_nanos() % other)

    def __divmod__(self: "Duration", other: int) -> tuple[int, "Duration"]:
        quo, rem = divmod(self.as_nanos(), other)
        return quo, Duration.from_nanos(rem)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return False
        return self.as_nanos() == other.as_nanos()

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return True
        return self.as_nanos() != other.as_nanos()

    def __lt__(self, other: "Duration") -> bool:
        return self.as_nanos() < other.as_nanos()

    def __le__(self, other: "Duration") -> bool:
        return self.as_nanos() <= other.as_nanos()

    def __gt__(self, other: "Duration") -> bool:
        return self.as_nanos() > other.as_nanos()

    def __ge__(self, other: "Duration") -> bool:
        return self.as_nanos() >= other.as_nanos()

    def __hash__(self) -> int:
        return hash(self.as_nanos())

    def __str__(self) -> str:
        ns = self.as_nanos()
        if ns < 1000:  # noqa: PLR2004
            return f"{ns}ns"
        us = ns // 1000
        if us < 1000:  # noqa: PLR2004
            return f"{us}.{ns % 1000:03}".rstrip("0") + "μs" if ns % 1000 != 0 else f"{us}μs"
        ms = us // 1000
        if ms < 1000:  # noqa: PLR2004
            return f"{ms}.{us % 1000:03}".rstrip("0") + "ms" if us % 1000 != 0 else f"{ms}ms"
        s = ms // 1000
        return f"{s}.{ms % 1000:03}".rstrip("0") + "s" if ms % 1000 != 0 else f"{s}s"


def into_option_duration(duration: Duration | None) -> OptionDuration:
    return OptionDuration(ctypes.c_bool(duration is not None), duration._inner if duration is not None else _Duration())
