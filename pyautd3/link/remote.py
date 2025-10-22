from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi_driver import LinkPtr
from pyautd3.native_methods.autd3capi_link_remote import NativeMethods as LinkRemote
from pyautd3.native_methods.autd3capi_link_remote import RemoteOption as RemoteOption_
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr
from pyautd3.utils.duration import Duration, into_option_duration


class RemoteOption:
    timeout: Duration | None

    def __init__(self: Self, *, timeout: Duration | None = None) -> None:
        self.timeout = timeout

    def _inner(self: Self) -> RemoteOption_:
        return RemoteOption_(
            into_option_duration(self.timeout),
        )


class Remote(Link):
    addr: str
    option: RemoteOption

    def __init__(self: Self, addr: str, option: RemoteOption) -> None:
        super().__init__()
        self.addr = addr
        self.option = option

    def _resolve(self: Self) -> LinkPtr:
        return _validate_ptr(LinkRemote().link_remote(_to_null_terminated_utf8(self.addr), self.option._inner()))  # pragma: no cover
