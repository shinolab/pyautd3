import ctypes
from collections.abc import Callable
from datetime import timedelta
from typing import Self

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import (
    NativeMethods as Base,
)
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr, SyncMode
from pyautd3.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM
from pyautd3.native_methods.autd3capi_link_soem import (
    ProcessPriority,
    ThreadPriorityPtr,
    TimerStrategy,
)
from pyautd3.native_methods.autd3capi_link_soem import Status as _Status
from pyautd3.native_methods.utils import ConstantADT, _validate_ptr

ErrHandlerFunc = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint8)  # type: ignore[arg-type]


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


class EtherCATAdapter:
    desc: str
    name: str

    def __init__(self: Self, name: str, desc: str) -> None:
        self.desc = desc
        self.name = name

    def __repr__(self: Self) -> str:
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
        err_handler: Callable[[int, Status], None] | None
        timer_strategy: TimerStrategy
        sync_mode: SyncMode
        sync_tolerance: timedelta
        sync_timeout: timedelta
        state_check_interval: timedelta
        process_priority: ProcessPriority
        thread_priority: ThreadPriorityPtr

        def __init__(self: Self) -> None:
            self.ifname = ""
            self.buf_size = 32
            self.send_cycle = timedelta(milliseconds=1)
            self.sync0_cycle = timedelta(milliseconds=1)
            self.err_handler = None
            self.timer_strategy = TimerStrategy.SpinSleep
            self.sync_mode = SyncMode.DC
            self.sync_tolerance = timedelta(microseconds=1)
            self.sync_timeout = timedelta(seconds=10)
            self.state_check_interval = timedelta(milliseconds=100)
            self.process_priority = ProcessPriority.High
            self.thread_priority = ThreadPriority.Max

        def with_ifname(self: Self, ifname: str) -> Self:
            self.ifname = ifname
            return self

        def with_buf_size(self: Self, buf_size: int) -> Self:
            self.buf_size = buf_size
            return self

        def with_send_cycle(self: Self, send_cycle: timedelta) -> Self:
            self.send_cycle = send_cycle
            return self

        def with_sync0_cycle(self: Self, sync0_cycle: timedelta) -> Self:
            self.sync0_cycle = sync0_cycle
            return self

        def with_sync_mode(self: Self, sync_mode: SyncMode) -> Self:
            self.sync_mode = sync_mode
            return self

        def with_timer_strategy(self: Self, timer_strategy: TimerStrategy) -> Self:
            self.timer_strategy = timer_strategy
            return self

        def with_sync_tolerance(self: Self, sync_tolerance: timedelta) -> Self:
            self.sync_tolerance = sync_tolerance
            return self

        def with_sync_timeout(self: Self, sync_timeout: timedelta) -> Self:
            self.sync_timeout = sync_timeout
            return self

        def with_state_check_interval(self: Self, state_check_interval: timedelta) -> Self:
            self.state_check_interval = state_check_interval
            return self

        def with_process_priority(self: Self, process_priority: ProcessPriority) -> Self:
            self.process_priority = process_priority
            return self

        def with_thread_priority(self: Self, thread_priority: ThreadPriorityPtr) -> Self:
            self.thread_priority = thread_priority
            return self

        def with_err_handler(self: Self, handler: Callable[[int, Status], None]) -> Self:
            self.err_handler = handler
            return self

        def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
            def callback_native(_context: ctypes.c_void_p, slave: ctypes.c_uint32, status: ctypes.c_uint8) -> None:  # pragma: no cover
                err = ctypes.create_string_buffer(128)  # pragma: no cover
                status_ = _Status(int(status))  # pragma: no cover
                LinkSOEM().link_soem_status_get_msg(status_, err)  # pragma: no cover
                self.err_handler(int(slave), Status.__private_new__(status_, err.value.decode("utf-8")))  # type: ignore[misc]  # pragma: no cover

            self._err_handler = ErrHandlerFunc(callback_native)  # pragma: no cover

            return _validate_ptr(  # pragma: no cover
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

        def _resolve_link(self: Self, handle: HandlePtr, ptr: ControllerPtr) -> "SOEM":
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

    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr, err_handler) -> None:  # noqa: ANN001
        super().__init__(handle, ptr)  # pragma: no cover
        self._err_handler = err_handler  # pragma: no cover

    @staticmethod
    def builder() -> _Builder:
        return SOEM._Builder()


class RemoteSOEM(Link):
    class _Builder(LinkBuilder["RemoteSOEM"]):
        addr: str

        def __init__(self: Self, addr: str) -> None:
            self.addr = addr

        def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
            return _validate_ptr(LinkSOEM().link_remote_soem(self.addr.encode("utf-8")))  # pragma: no cover

        def _resolve_link(self: Self, handle: HandlePtr, ptr: ControllerPtr) -> "RemoteSOEM":
            return RemoteSOEM(handle, Base().link_get(ptr))  # pragma: no cover

    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(addr: str) -> _Builder:
        return RemoteSOEM._Builder(addr)
