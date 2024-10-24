from typing import Self

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr
from pyautd3.native_methods.autd3capi_link_simulator import (
    NativeMethods as LinkSimulator,
)
from pyautd3.native_methods.utils import _validate_ptr


class Simulator(Link):
    class _Builder(LinkBuilder["Simulator"]):
        addr: str

        def __init__(self: Self, addr: str) -> None:
            self.addr = addr

        def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
            return _validate_ptr(LinkSimulator().link_simulator(self.addr.encode("utf-8")))  # pragma: no cover

        def _resolve_link(self: Self, handle: HandlePtr, ptr: ControllerPtr) -> "Simulator":
            return Simulator(handle, Base().link_get(ptr))  # pragma: no cover

    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(addr: str) -> _Builder:
        return Simulator._Builder(addr)
