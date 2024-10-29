from typing import Self

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr
from pyautd3.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM
from pyautd3.native_methods.utils import _validate_ptr


class _RemoteSOEMBuilder(LinkBuilder["RemoteSOEM"]):
    addr: str

    def __init__(self: Self, addr: str) -> None:
        self.addr = addr

    def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
        return _validate_ptr(LinkSOEM().link_remote_soem(self.addr.encode("utf-8")))  # pragma: no cover

    def _resolve_link(self: Self, handle: HandlePtr, ptr: ControllerPtr) -> "RemoteSOEM":
        return RemoteSOEM(handle, Base().link_get(ptr))  # pragma: no cover


class RemoteSOEM(Link):
    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(addr: str) -> _RemoteSOEMBuilder:
        return _RemoteSOEMBuilder(addr)
