import ctypes
from collections.abc import Callable
from datetime import timedelta

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import (
    NativeMethods as Base,
)
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr, SyncMode
from pyautd3.native_methods.autd3capi_link_soem import LinkRemoteSOEMBuilderPtr, LinkSOEMBuilderPtr, Status, TimerStrategy
from pyautd3.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM
from pyautd3.native_methods.utils import _validate_ptr

ErrHandlerFunc = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint8)  # type: ignore[arg-type]


class EtherCATAdapter:
    desc: str
    name: str

    def __init__(self: "EtherCATAdapter", name: str, desc: str) -> None:
        self.desc = desc
        self.name = name

    def __repr__(self: "EtherCATAdapter") -> str:
        return f"{self.desc}, {self.name}"


class SOEM(Link):
    class _Builder(LinkBuilder["SOEM"]):
        _builder: LinkSOEMBuilderPtr

        def __init__(self: "SOEM._Builder") -> None:
            self._builder = LinkSOEM().link_soem()

        def with_ifname(self: "SOEM._Builder", ifname: str) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_ifname(self._builder, ifname.encode("utf-8"))
            return self

        def with_buf_size(self: "SOEM._Builder", size: int) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_buf_size(self._builder, size)
            return self

        def with_send_cycle(self: "SOEM._Builder", cycle: int) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_send_cycle(self._builder, cycle)
            return self

        def with_sync0_cycle(self: "SOEM._Builder", cycle: int) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_sync_0_cycle(self._builder, cycle)
            return self

        def with_err_handler(self: "SOEM._Builder", handler: Callable[[int, Status, str], None]) -> "SOEM._Builder":
            def callback_native(_context: ctypes.c_void_p, slave: ctypes.c_uint32, status: ctypes.c_uint8) -> None:
                err = ctypes.create_string_buffer(128)  # pragma: no cover
                status_ = Status(int(status))  # pragma: no cover
                LinkSOEM().link_soem_status_get_msg(status_, err)  # pragma: no cover
                handler(int(slave), status_, err.value.decode("utf-8"))  # pragma: no cover

            self._err_handler = ErrHandlerFunc(callback_native)
            self._builder = LinkSOEM().link_soem_with_err_handler(self._builder, self._err_handler, None)  # type: ignore[arg-type]
            return self

        def with_timer_strategy(self: "SOEM._Builder", strategy: TimerStrategy) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_timer_strategy(self._builder, strategy)
            return self

        def with_sync_mode(self: "SOEM._Builder", mode: SyncMode) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_sync_mode(self._builder, mode)
            return self

        def with_sync_tolerance(self: "SOEM._Builder", tolerance: timedelta) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_sync_tolerance(self._builder, int(tolerance.total_seconds() * 1000 * 1000 * 1000))
            return self

        def with_sync_timeout(self: "SOEM._Builder", timeout: timedelta) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_sync_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def with_state_check_interval(self: "SOEM._Builder", interval: timedelta) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_state_check_interval(self._builder, int(interval.total_seconds() / 1000))
            return self

        def with_timeout(self: "SOEM._Builder", timeout: timedelta) -> "SOEM._Builder":
            self._builder = LinkSOEM().link_soem_with_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def _link_builder_ptr(self: "SOEM._Builder") -> LinkBuilderPtr:
            return LinkSOEM().link_soem_into_builder(self._builder)

        def _resolve_link(self: "SOEM._Builder", handle: HandlePtr, ptr: ControllerPtr) -> "SOEM":
            return SOEM(handle, Base().link_get(ptr), self._err_handler)  # pragma: no cover

    @staticmethod
    def enumerate_adapters() -> list[EtherCATAdapter]:
        handle = LinkSOEM().adapter_pointer()
        size = LinkSOEM().adapter_get_size(handle)

        def get_adapter(i: int) -> EtherCATAdapter:
            sb_desc = ctypes.create_string_buffer(128)
            sb_name = ctypes.create_string_buffer(128)
            LinkSOEM().adapter_get_adapter(handle, i, sb_desc, sb_name)
            return EtherCATAdapter(sb_name.value.decode("utf-8"), sb_desc.value.decode("utf-8"))

        res = list(map(get_adapter, range(int(size))))

        LinkSOEM().adapter_pointer_delete(handle)

        return res

    def __init__(self: "SOEM", handle: HandlePtr, ptr: LinkPtr, err_handler) -> None:  # noqa: ANN001
        super().__init__(handle, ptr)  # pragma: no cover
        self._err_handler = err_handler  # pragma: no cover

    @staticmethod
    def builder() -> _Builder:
        return SOEM._Builder()


class RemoteSOEM(Link):
    class _Builder(LinkBuilder["RemoteSOEM"]):
        _builder: LinkRemoteSOEMBuilderPtr

        def __init__(self: "RemoteSOEM._Builder", addr: str) -> None:
            self._builder = _validate_ptr(LinkSOEM().link_remote_soem(addr.encode("utf-8")))

        def with_timeout(self: "RemoteSOEM._Builder", timeout: timedelta) -> "RemoteSOEM._Builder":
            self._builder = LinkSOEM().link_remote_soem_with_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def _link_builder_ptr(self: "RemoteSOEM._Builder") -> LinkBuilderPtr:
            return LinkSOEM().link_remote_soem_into_builder(self._builder)  # pragma: no cover

        def _resolve_link(self: "RemoteSOEM._Builder", handle: HandlePtr, ptr: ControllerPtr) -> "RemoteSOEM":
            return RemoteSOEM(handle, Base().link_get(ptr))  # pragma: no cover

    def __init__(self: "RemoteSOEM", handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(addr: str) -> _Builder:
        return RemoteSOEM._Builder(addr)
