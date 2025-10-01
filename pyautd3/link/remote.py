from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi_driver import LinkPtr
from pyautd3.native_methods.autd3capi_link_remote import NativeMethods as LinkRemote
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr


class Remote(Link):
    addr: str

    def __init__(self: Self, addr: str) -> None:
        super().__init__()
        self.addr = addr

    def _resolve(self: Self) -> LinkPtr:
        return _validate_ptr(LinkRemote().link_remote(_to_null_terminated_utf8(self.addr)))  # pragma: no cover
