import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3 import Status
from pyautd3.native_methods.autd3capi_driver import Duration, ResultLink, ResultStatus


class ThreadPriorityPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ThreadPriorityPtr) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class EtherCrabOption(ctypes.Structure):
    _fields_ = [
        ("ifname", ctypes.c_char_p),
        ("buf_size", ctypes.c_uint32),
        ("timeouts_state_transition", Duration),
        ("timeouts_pdu", Duration),
        ("timeouts_eeprom", Duration),
        ("timeouts_wait_loop_delay", Duration),
        ("timeouts_mailbox_echo", Duration),
        ("timeouts_mailbox_response", Duration),
        ("main_device_config_dc_static_sync_iterations", ctypes.c_uint32),
        ("main_device_config_retry_behaviour", ctypes.c_uint64),
        ("dc_configuration_start_delay", Duration),
        ("dc_configuration_sync0_period", Duration),
        ("dc_configuration_sync0_shift", Duration),
        ("state_check_period", Duration),
        ("sync_tolerance", Duration),
        ("sync_timeout", Duration),
        ("tx_rx_thread_builder", ThreadPriorityPtr),
        ("tx_rx_thread_affinity", ctypes.c_int32),
        ("main_thread_builder", ThreadPriorityPtr),
        ("main_thread_affinity", ctypes.c_int32),
    ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EtherCrabOption) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class Singleton(type):
    _instances = {}  # type: ignore[var-annotated]
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:  # pragma: no cover
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):
    def init_dll(self, bin_location: Path, bin_prefix: str, bin_ext: str) -> None:
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi_link_ethercrab{bin_ext}"))

        self.dll.AUTDLinkEtherCrabTracingInit.argtypes = []
        self.dll.AUTDLinkEtherCrabTracingInit.restype = None

        self.dll.AUTDLinkEtherCrabTracingInitWithFile.argtypes = [ctypes.c_char_p]
        self.dll.AUTDLinkEtherCrabTracingInitWithFile.restype = ResultStatus

        self.dll.AUTDLinkEtherCrab.argtypes = [ctypes.c_void_p, ctypes.c_void_p, EtherCrabOption]
        self.dll.AUTDLinkEtherCrab.restype = ResultLink

        self.dll.AUTDLinkEtherCrabIsDefault.argtypes = [EtherCrabOption]
        self.dll.AUTDLinkEtherCrabIsDefault.restype = ctypes.c_bool

        self.dll.AUTDLinkEtherCrabStatusGetMsg.argtypes = [ctypes.c_uint8, ctypes.c_char_p]
        self.dll.AUTDLinkEtherCrabStatusGetMsg.restype = ctypes.c_uint32

        self.dll.AUTDLinkEtherCrabThreadPriorityMin.argtypes = []
        self.dll.AUTDLinkEtherCrabThreadPriorityMin.restype = ThreadPriorityPtr

        self.dll.AUTDLinkEtherCrabThreadPriorityCrossplatform.argtypes = [ctypes.c_uint8]
        self.dll.AUTDLinkEtherCrabThreadPriorityCrossplatform.restype = ThreadPriorityPtr

        self.dll.AUTDLinkEtherCrabThreadPriorityMax.argtypes = []
        self.dll.AUTDLinkEtherCrabThreadPriorityMax.restype = ThreadPriorityPtr

    def link_ether_crab_tracing_init(self) -> None:
        return self.dll.AUTDLinkEtherCrabTracingInit()

    def link_ether_crab_tracing_init_with_file(self, path: bytes) -> ResultStatus:
        return self.dll.AUTDLinkEtherCrabTracingInitWithFile(path)

    def link_ether_crab(self, err_handler: ctypes.c_void_p, err_context: ctypes.c_void_p, option: EtherCrabOption) -> ResultLink:
        return self.dll.AUTDLinkEtherCrab(err_handler, err_context, option)

    def link_ether_crab_is_default(self, option: EtherCrabOption) -> ctypes.c_bool:
        return self.dll.AUTDLinkEtherCrabIsDefault(option)

    def link_ether_crab_status_get_msg(self, src: Status, dst: bytes) -> ctypes.c_uint32:
        return self.dll.AUTDLinkEtherCrabStatusGetMsg(src, dst)

    def link_ether_crab_thread_priority_min(self) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkEtherCrabThreadPriorityMin()

    def link_ether_crab_thread_priority_crossplatform(self, value: int) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkEtherCrabThreadPriorityCrossplatform(value)

    def link_ether_crab_thread_priority_max(self) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkEtherCrabThreadPriorityMax()
