import ctypes
from collections.abc import Callable
from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi_driver import LinkPtr
from pyautd3.native_methods.autd3capi_link_ethercrab import EtherCrabOption as EtherCrabOption_
from pyautd3.native_methods.autd3capi_link_ethercrab import NativeMethods as LinkEtherCrab
from pyautd3.native_methods.autd3capi_link_ethercrab import Status as Status_
from pyautd3.native_methods.autd3capi_link_ethercrab import ThreadPriorityPtr
from pyautd3.native_methods.utils import ConstantADT, _to_null_terminated_utf8, _validate_ptr
from pyautd3.utils import Duration

ErrHandlerFunc = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint8)  # type: ignore[arg-type]


class CoreId:
    id: int

    def __init__(self, id_: int) -> None:
        self.id = id_


class ThreadPriority(metaclass=ConstantADT):
    Min: ThreadPriorityPtr = LinkEtherCrab().link_ether_crab_thread_priority_min()
    Max: ThreadPriorityPtr = LinkEtherCrab().link_ether_crab_thread_priority_max()

    @staticmethod
    def Crossplatform(value: int) -> ThreadPriorityPtr:  # noqa: N802
        if not (0 <= value <= 99):  # noqa: PLR2004
            msg = "value must be between 0 and 99"
            raise ValueError(msg)
        return LinkEtherCrab().link_ether_crab_thread_priority_crossplatform(value)


class Status(metaclass=ConstantADT):
    _inner: Status_
    _msg: str

    @classmethod
    def __private_new__(cls: type["Status"], inner: Status_, msg: str) -> "Status":
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

    def __hash__(self: Self) -> int:
        return self._inner.__hash__()  # pragma: no cover

    @staticmethod
    def Lost() -> "Status":  # noqa: N802
        return Status.__private_new__(Status_.Lost, "")

    @staticmethod
    def StateChanged() -> "Status":  # noqa: N802
        return Status.__private_new__(Status_.StateChanged, "")

    @staticmethod
    def Error() -> "Status":  # noqa: N802
        return Status.__private_new__(Status_.Error, "")

    @staticmethod
    def Resumed() -> "Status":  # noqa: N802
        return Status.__private_new__(Status_.Resumed, "")


def tracing_init() -> None:
    LinkEtherCrab().link_ether_crab_tracing_init()


class EtherCrabOption:
    ifname: str | None
    buf_size: int
    state_check_period: Duration
    sync0_period: Duration
    sync_tolerance: Duration
    sync_timeout: Duration
    tx_rx_thread_builder: ThreadPriorityPtr | None
    tx_rx_thread_affinity: CoreId | None
    main_thread_builder: ThreadPriorityPtr | None
    main_thread_affinity: CoreId | None

    def __init__(
        self: Self,
        *,
        ifname: str | None = None,
        buf_size: int = 16,
        state_check_period: Duration | None = None,
        sync0_period: Duration | None = None,
        sync_tolerance: Duration | None = None,
        sync_timeout: Duration | None = None,
        tx_rx_thread_builder: ThreadPriorityPtr | None = None,
        tx_rx_thread_affinity: CoreId | None = None,
        main_thread_builder: ThreadPriorityPtr | None = None,
        main_thread_affinity: CoreId | None = None,
    ) -> None:
        self.ifname = ifname
        self.buf_size = buf_size
        self.state_check_period = state_check_period or Duration.from_millis(100)
        self.sync0_period = sync0_period or Duration.from_millis(2)
        self.sync_tolerance = sync_tolerance or Duration.from_micros(1)
        self.sync_timeout = sync_timeout or Duration.from_secs(10)
        self.tx_rx_thread_builder = tx_rx_thread_builder
        self.tx_rx_thread_affinity = tx_rx_thread_affinity
        self.main_thread_builder = main_thread_builder
        self.main_thread_affinity = main_thread_affinity

    def _inner(self: Self) -> EtherCrabOption_:
        return EtherCrabOption_(
            _to_null_terminated_utf8(self.ifname) if self.ifname else None,
            self.buf_size,
            Duration.from_secs(10)._inner,  # state_transition
            Duration.from_millis(100)._inner,  # pdu
            Duration.from_millis(10)._inner,  # eeprom
            Duration.from_millis(0)._inner,  # wait_loop_delay
            Duration.from_millis(100)._inner,  # mailbox_echo
            Duration.from_millis(1000)._inner,  # mailbox_response
            10000,  # dc_static_sync_iterations
            0,  # retry_behaviour
            Duration.from_millis(100)._inner,  # start_delay
            self.sync0_period._inner,
            Duration.from_micros(0)._inner,  # sync0_shift
            self.state_check_period._inner,
            self.sync_tolerance._inner,
            self.sync_timeout._inner,
            self.tx_rx_thread_builder or ThreadPriorityPtr(None),
            self.tx_rx_thread_affinity.id if self.tx_rx_thread_affinity else -1,
            self.main_thread_builder or ThreadPriorityPtr(None),
            self.main_thread_affinity.id if self.main_thread_affinity else -1,
        )


class EtherCrab(Link):
    _err_handler: Callable[[int, Status], None]
    _option: EtherCrabOption

    def __init__(self: Self, err_handler: Callable[[int, Status], None], option: EtherCrabOption) -> None:
        super().__init__()
        self._err_handler = err_handler
        self._option = option

    def _resolve(self: Self) -> LinkPtr:
        def callback_native(_context: ctypes.c_void_p, slave: ctypes.c_uint32, status: ctypes.c_uint8) -> None:  # pragma: no cover
            err = bytes(bytearray(128))  # pragma: no cover
            status_ = Status_(int(status))  # pragma: no cover
            LinkEtherCrab().link_ether_crab_status_get_msg(status_, err)  # pragma: no cover
            self._err_handler(int(slave), Status.__private_new__(status_, err.decode("utf-8").rstrip(" \t\r\n\0")))  # pragma: no cover

        self._err_handler_f = ErrHandlerFunc(callback_native)  # pragma: no cover

        return _validate_ptr(  # pragma: no cover
            LinkEtherCrab().link_ether_crab(
                self._err_handler_f,  # type: ignore[arg-type]
                ctypes.c_void_p(0),
                self._option._inner(),
            ),
        )
