from datetime import timedelta

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkPtr
from pyautd3.native_methods.autd3capi_link_simulator import (
    LinkBuilderPtr,
    LinkSimulatorBuilderPtr,
)
from pyautd3.native_methods.autd3capi_link_simulator import (
    NativeMethods as LinkSimulator,
)
from pyautd3.native_methods.utils import _validate_ptr


class Simulator(Link):
    class _Builder(LinkBuilder["Simulator"]):
        _builder: LinkSimulatorBuilderPtr

        def __init__(self: "Simulator._Builder", addr: str) -> None:
            self._builder = _validate_ptr(LinkSimulator().link_simulator(addr.encode("utf-8")))

        def with_timeout(self: "Simulator._Builder", timeout: timedelta) -> "Simulator._Builder":
            self._builder = LinkSimulator().link_simulator_with_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def _link_builder_ptr(self: "Simulator._Builder") -> LinkBuilderPtr:
            return LinkSimulator().link_simulator_into_builder(self._builder)  # pragma: no cover

        def _resolve_link(self: "Simulator._Builder", handle: HandlePtr, ptr: ControllerPtr) -> "Simulator":
            return Simulator(handle, Base().link_get(ptr))  # pragma: no cover

    def __init__(self: "Simulator", handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(addr: str) -> _Builder:
        return Simulator._Builder(addr)
