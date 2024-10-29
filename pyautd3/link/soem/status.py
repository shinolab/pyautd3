from typing import Self

from pyautd3.native_methods.autd3capi_link_soem import Status as _Status
from pyautd3.native_methods.utils import ConstantADT


class Status(metaclass=ConstantADT):
    _inner: _Status
    _msg: str

    @classmethod
    def __private_new__(cls: type["Status"], inner: _Status, msg: str) -> "Status":
        ins = super().__new__(cls)
        ins._inner = inner
        ins._msg = msg
        return ins

    def __new__(cls: type["Status"]) -> "Status":
        raise NotImplementedError

    def __repr__(self: Self) -> str:
        return f"{self._msg}"

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, Status):
            return False
        return self._inner == other._inner

    @staticmethod
    def Lost() -> "Status":  # noqa: N802
        return Status.__private_new__(_Status.Lost, "")

    @staticmethod
    def StateChanged() -> "Status":  # noqa: N802
        return Status.__private_new__(_Status.StateChanged, "")

    @staticmethod
    def Error() -> "Status":  # noqa: N802
        return Status.__private_new__(_Status.Error, "")
