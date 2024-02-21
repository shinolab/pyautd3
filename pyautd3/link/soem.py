import ctypes
from collections.abc import Callable
from datetime import timedelta

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import (
    NativeMethods as Base,
)
from pyautd3.native_methods.autd3capi_def import ControllerPtr, LinkBuilderPtr, LinkPtr, TimerStrategy
from pyautd3.native_methods.autd3capi_link_soem import LinkRemoteSOEMBuilderPtr, LinkSOEMBuilderPtr, Status, SyncMode
from pyautd3.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM
from pyautd3.native_methods.utils import _validate_ptr

ErrHandlerFunc = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_char_p)  # type: ignore[arg-type]


class EtherCATAdapter:
    """Ethernet adapter."""

    desc: str
    """Description of the adapter"""

    name: str
    """Name of the adapter"""

    def __init__(self: "EtherCATAdapter", name: str, desc: str) -> None:
        self.desc = desc
        self.name = name

    def __repr__(self: "EtherCATAdapter") -> str:
        return f"{self.desc}, {self.name}"


class SOEM(Link):
    """Link using SOEM."""

    class _Builder(LinkBuilder):
        _builder: LinkSOEMBuilderPtr

        def __init__(self: "SOEM._Builder") -> None:
            self._builder = LinkSOEM().link_soem()

        def with_ifname(self: "SOEM._Builder", ifname: str) -> "SOEM._Builder":
            """Set network interface name.

            Arguments:
            ---------
                ifname: Network interface name (e.g. "eth0").
                        If empty, this link will automatically find the network interface that is connected to AUTD3 devices.

            """
            self._builder = LinkSOEM().link_soem_with_ifname(self._builder, ifname.encode("utf-8"))
            return self

        def with_buf_size(self: "SOEM._Builder", size: int) -> "SOEM._Builder":
            """Set send buffer size.

            Arguments:
            ---------
                size: Send buffer size

            """
            self._builder = LinkSOEM().link_soem_with_buf_size(self._builder, size)
            return self

        def with_send_cycle(self: "SOEM._Builder", cycle: int) -> "SOEM._Builder":
            """Set send cycle.

            Arguments:
            ---------
                cycle: Send cycle (the unit is 500us)

            """
            self._builder = LinkSOEM().link_soem_with_send_cycle(self._builder, cycle)
            return self

        def with_sync0_cycle(self: "SOEM._Builder", cycle: int) -> "SOEM._Builder":
            """Set sync0 cycle.

            Arguments:
            ---------
                cycle: Sync0 cycle (the unit is 500us)

            """
            self._builder = LinkSOEM().link_soem_with_sync_0_cycle(self._builder, cycle)
            return self

        def with_err_handler(self: "SOEM._Builder", handler: Callable[[int, Status, str], None]) -> "SOEM._Builder":
            """Set callback function when some error occurs.

            Arguments:
            ---------
                handler: Callback function

            """

            def callback_native(_context: ctypes.c_void_p, slave: ctypes.c_uint32, status: ctypes.c_uint8, p_msg: bytes) -> None:
                handler(int(slave), Status(int(status)), p_msg.decode("utf-8"))  # pragma: no cover

            self._err_handler = ErrHandlerFunc(callback_native)
            self._builder = LinkSOEM().link_soem_with_err_handler(self._builder, self._err_handler, None)  # type: ignore[arg-type]
            return self

        def with_timer_strategy(self: "SOEM._Builder", strategy: TimerStrategy) -> "SOEM._Builder":
            """Set timer strategy.

            Arguments:
            ---------
                strategy: Timer strategy

            """
            self._builder = LinkSOEM().link_soem_with_timer_strategy(self._builder, strategy)
            return self

        def with_sync_mode(self: "SOEM._Builder", mode: SyncMode) -> "SOEM._Builder":
            """Set sync mode.

            See [Beckhoff's site](https://infosys.beckhoff.com/content/1033/ethercatsystem/2469122443.html) for more details.

            Arguments:
            ---------
                mode: Sync mode

            """
            self._builder = LinkSOEM().link_soem_with_sync_mode(self._builder, mode)
            return self

        def with_state_check_interval(self: "SOEM._Builder", interval: timedelta) -> "SOEM._Builder":
            """Set state check interval.

            Arguments:
            ---------
                interval: State check interval

            """
            self._builder = LinkSOEM().link_soem_with_state_check_interval(self._builder, int(interval.total_seconds() / 1000))
            return self

        def with_timeout(self: "SOEM._Builder", timeout: timedelta) -> "SOEM._Builder":
            """Set timeout.

            Arguments:
            ---------
                timeout: Timeout

            """
            self._builder = LinkSOEM().link_soem_with_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def _link_builder_ptr(self: "SOEM._Builder") -> LinkBuilderPtr:
            return LinkSOEM().link_soem_into_builder(self._builder)

        def _resolve_link(self: "SOEM._Builder", _ptr: ControllerPtr) -> "SOEM":
            return SOEM(Base().link_get(_ptr), self._err_handler)  # pragma: no cover

    @staticmethod
    def enumerate_adapters() -> list[EtherCATAdapter]:
        """Enumerate ethernet adapters."""
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

    def __init__(self: "SOEM", ptr: LinkPtr, err_handler) -> None:  # noqa: ANN001
        super().__init__(ptr)  # pragma: no cover
        self._err_handler = err_handler  # pragma: no cover

    @staticmethod
    def builder() -> _Builder:
        """Create SOEM link builder."""
        return SOEM._Builder()


class RemoteSOEM(Link):
    """Link to connect to remote SOEMServer."""

    class _Builder(LinkBuilder):
        _builder: LinkRemoteSOEMBuilderPtr

        def __init__(self: "RemoteSOEM._Builder", addr: str) -> None:
            self._builder = _validate_ptr(LinkSOEM().link_remote_soem(addr.encode("utf-8")))

        def with_timeout(self: "RemoteSOEM._Builder", timeout: timedelta) -> "RemoteSOEM._Builder":
            """Set timeout.

            Arguments:
            ---------
                timeout: Timeout

            """
            self._builder = LinkSOEM().link_remote_soem_with_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def _link_builder_ptr(self: "RemoteSOEM._Builder") -> LinkBuilderPtr:
            return LinkSOEM().link_remote_soem_into_builder(self._builder)  # pragma: no cover

        def _resolve_link(self: "RemoteSOEM._Builder", _ptr: ControllerPtr) -> "RemoteSOEM":
            return RemoteSOEM(Base().link_get(_ptr))  # pragma: no cover

    def __init__(self: "RemoteSOEM", ptr: LinkPtr) -> None:
        super().__init__(ptr)  # pragma: no cover

    @staticmethod
    def builder(addr: str) -> _Builder:
        """Create RemoteSOEM link builder.

        Arguments:
        ---------
            addr: IP address and port of SOEMServer (e.g. "127.0.0.1:8080")

        """
        return RemoteSOEM._Builder(addr)
