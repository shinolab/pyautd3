from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi_driver import LinkPtr
from pyautd3.native_methods.autd3capi_link_simulator import NativeMethods as LinkSimulator
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr


class Simulator(Link):
    addr: str

    def __init__(self: Self, addr: str) -> None:
        super().__init__()
        self.addr = addr

    def _resolve(self: Self) -> LinkPtr:
        return _validate_ptr(LinkSimulator().link_simulator(_to_null_terminated_utf8(self.addr)))  # pragma: no cover
