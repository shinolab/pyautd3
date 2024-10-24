import ctypes
from collections.abc import Callable
from datetime import timedelta

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import (
    NativeMethods as Base,
)
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr, SyncMode
from pyautd3.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM
from pyautd3.native_methods.autd3capi_link_soem import (
    ProcessPriority,
    Status,
    ThreadPriorityPtr,
    TimerStrategy,
)
from pyautd3.native_methods.utils import ConstantADT, _validate_ptr

ErrHandlerFunc = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint8)  # type: ignore[arg-type]


class EtherCATAdapter:
    desc: str
    name: str

    def __init__(self: "EtherCATAdapter", name: str, desc: str) -> None:
        self.desc = desc
        self.name = name

    def __repr__(self: "EtherCATAdapter") -> str:
        return f"{self.desc}, {self.name}"


class ThreadPriority(metaclass=ConstantADT):
    Min: ThreadPriorityPtr = LinkSOEM().link_soem_thread_priority_min()
    Max: ThreadPriorityPtr = LinkSOEM().link_soem_thread_priority_max()

    @staticmethod
    def Crossplatform(value: int) -> ThreadPriorityPtr:  # noqa: N802
        if not (0 <= value <= 99):  # noqa: PLR2004
            msg = "value must be between 0 and 99"
            raise ValueError(msg)
        return LinkSOEM().link_soem_thread_priority_crossplatform(value)


class SOEM(Link):
    class _Builder(LinkBuilder["SOEM"]):
        ifname: str
        buf_size: int
        send_cycle: timedelta
        sync0_cycle: timedelta
        err_handler: Callable[[int, Status, str], None] | None
        timer_strategy: TimerStrategy
        sync_mode: SyncMode
        sync_tolerance: timedelta
        sync_timeout: timedelta
        state_check_interval: timedelta
        process_priority: ProcessPriority
        thread_priority: ThreadPriorityPtr

        def __init__(self: "SOEM._Builder") -> None:
            self.ifname = ""
            self.buf_size = 32
            self.send_cycle = timedelta(milliseconds=1)
            self.sync0_cycle = timedelta(milliseconds=1)
            self.err_handler = None
            self.timer_strategy = TimerStrategy.SpinSleep
            self.sync_mode = SyncMode.DC
            self.sync_tolerance = timedelta(microseconds=100)
            self.sync_timeout = timedelta(seconds=10)
            self.state_check_interval = timedelta(milliseconds=100)
            self.process_priority = ProcessPriority.High
            self.thread_priority = ThreadPriority.Max

        def with_ifname(self: "SOEM._Builder", ifname: str) -> "SOEM._Builder":
            self.ifname = ifname
            return self

        def with_buf_size(self: "SOEM._Builder", buf_size: int) -> "SOEM._Builder":
            self.buf_size = buf_size
            return self

        def with_send_cycle(self: "SOEM._Builder", send_cycle: timedelta) -> "SOEM._Builder":
            self.send_cycle = send_cycle
            return self

        def with_sync0_cycle(self: "SOEM._Builder", sync0_cycle: timedelta) -> "SOEM._Builder":
            self.sync0_cycle = sync0_cycle
            return self

        def with_sync_mode(self: "SOEM._Builder", sync_mode: SyncMode) -> "SOEM._Builder":
            self.sync_mode = sync_mode
            return self

        def with_timer_strategy(self: "SOEM._Builder", timer_strategy: TimerStrategy) -> "SOEM._Builder":
            self.timer_strategy = timer_strategy
            return self

        def with_sync_tolerance(self: "SOEM._Builder", sync_tolerance: timedelta) -> "SOEM._Builder":
            self.sync_tolerance = sync_tolerance
            return self

        def with_sync_timeout(self: "SOEM._Builder", sync_timeout: timedelta) -> "SOEM._Builder":
            self.sync_timeout = sync_timeout
            return self

        def with_state_check_interval(self: "SOEM._Builder", state_check_interval: timedelta) -> "SOEM._Builder":
            self.state_check_interval = state_check_interval
            return self

        def with_process_priority(self: "SOEM._Builder", process_priority: ProcessPriority) -> "SOEM._Builder":
            self.process_priority = process_priority
            return self

        def with_thread_priority(self: "SOEM._Builder", thread_priority: ThreadPriorityPtr) -> "SOEM._Builder":
            self.thread_priority = thread_priority
            return self

        def with_err_handler(self: "SOEM._Builder", handler: Callable[[int, Status, str], None]) -> "SOEM._Builder":
            self.err_handler = handler
            return self

        def _link_builder_ptr(self: "SOEM._Builder") -> LinkBuilderPtr:
            def callback_native(_context: ctypes.c_void_p, slave: ctypes.c_uint32, status: ctypes.c_uint8) -> None:
                err = ctypes.create_string_buffer(128)  # pragma: no cover
                status_ = Status(int(status))  # pragma: no cover
                LinkSOEM().link_soem_status_get_msg(status_, err)  # pragma: no cover
                self.err_handler(int(slave), status_, err.value.decode("utf-8"))  # type: ignore[misc]  # pragma: no cover

            self._err_handler = ErrHandlerFunc(callback_native)

            return _validate_ptr(
                LinkSOEM().link_soem(
                    self.ifname.encode("utf-8"),
                    self.buf_size,
                    int(self.send_cycle.total_seconds() * 1000 * 1000 * 1000),
                    int(self.sync0_cycle.total_seconds() * 1000 * 1000 * 1000),
                    None if self.err_handler is None else self._err_handler,  # type: ignore[arg-type]
                    None,
                    self.sync_mode,
                    self.process_priority,
                    self.thread_priority,
                    int(self.state_check_interval.total_seconds() * 1000 * 1000 * 1000),
                    self.timer_strategy,
                    int(self.sync_tolerance.total_seconds() * 1000 * 1000 * 1000),
                    int(self.sync_timeout.total_seconds() * 1000 * 1000 * 1000),
                ),
            )

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
        addr: str

        def __init__(self: "RemoteSOEM._Builder", addr: str) -> None:
            self.addr = addr

        def _link_builder_ptr(self: "RemoteSOEM._Builder") -> LinkBuilderPtr:
            return _validate_ptr(LinkSOEM().link_remote_soem(self.addr.encode("utf-8")))  # pragma: no cover

        def _resolve_link(self: "RemoteSOEM._Builder", handle: HandlePtr, ptr: ControllerPtr) -> "RemoteSOEM":
            return RemoteSOEM(handle, Base().link_get(ptr))  # pragma: no cover

    def __init__(self: "RemoteSOEM", handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(addr: str) -> _Builder:
        return RemoteSOEM._Builder(addr)
