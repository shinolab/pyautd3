import ctypes
from collections.abc import Callable, Iterable
from types import TracebackType
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.autd_error import InvalidDatagramTypeError
from pyautd3.controller.sleeper import SpinSleeper, StdSleeper, WaitableSleeper
from pyautd3.driver.autd3_device import AUTD3
from pyautd3.driver.datagram import Datagram
from pyautd3.driver.firmware.fpga import FPGAState
from pyautd3.driver.firmware_version import FirmwareInfo
from pyautd3.driver.geometry import Device, Geometry
from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3 import ParallelMode
from pyautd3.native_methods.autd3capi import ControllerPtr, SenderPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SenderOption as SenderOption_
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr
from pyautd3.native_methods.structs import Point3, Quaternion
from pyautd3.native_methods.utils import _validate_ptr, _validate_status
from pyautd3.utils import Duration
from pyautd3.utils.duration import into_option_duration

K = TypeVar("K")
L = TypeVar("L", bound=Link)


class SenderOption:
    send_interval: Duration
    receive_interval: Duration
    timeout: Duration | None
    parallel: ParallelMode
    sleeper: StdSleeper | SpinSleeper | WaitableSleeper

    def __init__(
        self: Self,
        *,
        send_interval: Duration | None = None,
        receive_interval: Duration | None = None,
        timeout: Duration | None = None,
        parallel: ParallelMode = ParallelMode.Auto,
        sleeper: StdSleeper | SpinSleeper | WaitableSleeper | None = None,
    ) -> None:
        self.send_interval = send_interval or Duration.from_millis(1)
        self.receive_interval = receive_interval or Duration.from_millis(1)
        self.timeout = timeout
        self.parallel = parallel
        self.sleeper = sleeper or SpinSleeper()

    def _inner(self: Self) -> SenderOption_:
        return SenderOption_(
            self.send_interval._inner,
            self.receive_interval._inner,
            into_option_duration(self.timeout),
            self.parallel,
            self.sleeper._inner(),
        )


class Sender:
    _ptr: SenderPtr
    _geometry: Geometry

    def __init__(self: Self, ptr: SenderPtr, geometry: Geometry) -> None:
        self._ptr = ptr
        self._geometry = geometry

    def send(
        self: Self,
        d: Datagram | tuple[Datagram, Datagram],
    ) -> None:
        match d:
            case Datagram():
                result = Base().sender_send(self._ptr, d._datagram_ptr(self._geometry))
            case (Datagram(), Datagram()):
                (d1, d2) = d
                d_tuple = Base().datagram_tuple(d1._datagram_ptr(self._geometry), d2._datagram_ptr(self._geometry))
                result = Base().sender_send(self._ptr, d_tuple)
            case _:
                raise InvalidDatagramTypeError
        _validate_status(result)

    def group_send(
        self: Self,
        key_map: Callable[[Device], K | None],
        data_map: dict[K, Datagram | tuple[Datagram, Datagram]],
    ) -> None:
        keymap: dict[K, int] = {}
        datagrams: np.ndarray = np.ndarray(len(data_map), dtype=DatagramPtr)
        keys = np.arange(len(data_map), dtype=np.int32)

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int) -> int:
            dev = Device(dev_idx, geometry_ptr)
            key = key_map(dev)
            return keymap[key] if key is not None else -1

        f_native_ = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, GeometryPtr, ctypes.c_uint16)(f_native)

        for k, (key, d) in enumerate(data_map.items()):
            match d:
                case Datagram():
                    ptr = d._datagram_ptr(self._geometry)
                    datagrams[k]["value"] = ptr.value
                case (Datagram(), Datagram()):
                    (d1, d2) = d
                    ptr = Base().datagram_tuple(
                        d1._datagram_ptr(self._geometry),
                        d2._datagram_ptr(self._geometry),
                    )
                    datagrams[k]["value"] = ptr.value
                case _:
                    raise InvalidDatagramTypeError
            keymap[key] = k

        _validate_status(
            Base().controller_group(
                self._ptr,
                f_native_,  # type: ignore[arg-type]
                ctypes.c_void_p(0),
                self._geometry._geometry_ptr,
                keys.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),  # type: ignore[arg-type]
                datagrams.ctypes.data_as(ctypes.POINTER(DatagramPtr)),  # type: ignore[arg-type]
                len(keys),
            ),
        )


class Controller(Geometry, Generic[L]):
    _ptr: ControllerPtr
    _link: L
    _disposed: bool

    def __init__(self: Self, geometry: GeometryPtr, ptr: ControllerPtr, link: L) -> None:
        super().__init__(geometry)
        self._ptr = ptr
        self._link = link
        self._link._ptr = Base().link_get(self._ptr)
        self._disposed = False

    def link(self: Self) -> L:
        return self._link

    def __del__(self: Self) -> None:
        self._dispose()

    def _dispose(self: Self) -> None:
        self.close()

    def __enter__(self: Self) -> "Controller[L]":
        return self

    def __exit__(
        self: Self,
        _exc_type: type[BaseException] | None,
        _exc_value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        self._dispose()

    def geometry(self: Self) -> Geometry:
        return self  # type: ignore[return-value]

    @staticmethod
    def open(devices: Iterable[AUTD3], link: L) -> "Controller[L]":
        return Controller.open_with_option(devices, link, SenderOption())

    @staticmethod
    def open_with_option(devices: Iterable[AUTD3], link: L, option: SenderOption) -> "Controller[L]":
        devices = list(devices)
        pos = np.fromiter((np.void(Point3(d.pos)) for d in devices), dtype=Point3)  # type: ignore[type-var,call-overload]
        rot = np.fromiter((np.void(Quaternion(d.rot)) for d in devices), dtype=Quaternion)  # type: ignore[type-var,call-overload]

        ptr = _validate_ptr(
            Base().controller_open(
                pos.ctypes.data_as(ctypes.POINTER(Point3)),  # type: ignore[arg-type]
                rot.ctypes.data_as(ctypes.POINTER(Quaternion)),  # type: ignore[arg-type]
                len(devices),
                link._resolve(),
                option._inner(),
            ),
        )
        geometry = Base().geometry(ptr)
        return Controller(geometry, ptr, link)

    def firmware_version(self: Self) -> list[FirmwareInfo]:
        handle = _validate_ptr(
            Base().controller_firmware_version_list_pointer(self._ptr),
        )

        def get_firmware_info(i: int) -> FirmwareInfo:
            sb = bytes(bytearray(256))
            Base().controller_firmware_version_get(handle, i, sb)
            info = sb.decode("utf-8").rstrip(" \t\r\n\0")
            return FirmwareInfo(info)

        res = list(map(get_firmware_info, range(self.num_devices())))
        Base().controller_firmware_version_list_pointer_delete(handle)
        return res

    def close(self: Self) -> None:
        if self._disposed:
            return
        self._disposed = True
        r = Base().controller_close(self._ptr)
        self._ptr.value = None
        _validate_status(r)

    def fpga_state(self: Self) -> list[FPGAState | None]:
        handle = _validate_ptr(Base().controller_fpga_state(self._ptr))

        def get_fpga_state(i: int) -> FPGAState | None:
            state = int(Base().controller_fpga_state_get(handle, i))
            return None if state == -1 else FPGAState(state)

        res = list(map(get_fpga_state, range(self.num_devices())))
        Base().controller_fpga_state_delete(handle)
        return res

    def sender(self: Self, option: SenderOption) -> Sender:
        return Sender(Base().sender(self._ptr, option._inner()), self.geometry())

    def send(
        self: Self,
        d: Datagram | tuple[Datagram, Datagram],
    ) -> None:
        self.sender(SenderOption()).send(d)

    def group_send(
        self: Self,
        key_map: Callable[[Device], K | None],
        data_map: dict[K, Datagram | tuple[Datagram, Datagram]],
    ) -> None:
        self.sender(SenderOption()).group_send(key_map, data_map)
