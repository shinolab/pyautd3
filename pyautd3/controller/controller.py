import ctypes
from collections.abc import Iterable
from types import TracebackType
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.autd_error import InvalidDatagramTypeError
from pyautd3.controller.sleeper import SpinSleeper, StdSleeper, WaitableSleeper
from pyautd3.driver.autd3_device import AUTD3
from pyautd3.driver.datagram import Datagram
from pyautd3.driver.firmware.fpga import FPGAState
from pyautd3.driver.firmware_version import FirmwareInfo
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3 import ParallelMode
from pyautd3.native_methods.autd3capi import ControllerPtr, SenderPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SenderOption as SenderOption_
from pyautd3.native_methods.autd3capi_driver import GeometryPtr
from pyautd3.native_methods.structs import Point3, Quaternion
from pyautd3.native_methods.utils import _validate_ptr, _validate_status
from pyautd3.utils import Duration
from pyautd3.utils.duration import into_option_duration

L = TypeVar("L", bound=Link)

DEFAULT_TIMEOUT = Duration.from_millis(200)


class SenderOption:
    send_interval: Duration
    receive_interval: Duration
    timeout: Duration | None
    parallel: ParallelMode

    def __init__(
        self: Self,
        *,
        send_interval: Duration | None = None,
        receive_interval: Duration | None = None,
        timeout: Duration | None = DEFAULT_TIMEOUT,
        parallel: ParallelMode = ParallelMode.Auto,
    ) -> None:
        self.send_interval = send_interval or Duration.from_millis(1)
        self.receive_interval = receive_interval or Duration.from_millis(1)
        self.timeout = timeout
        self.parallel = parallel

    def _inner(self: Self) -> SenderOption_:
        return SenderOption_(
            self.send_interval._inner,
            self.receive_interval._inner,
            into_option_duration(self.timeout),
            self.parallel,
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


class Controller(Geometry, Generic[L]):
    _ptr: ControllerPtr
    _link: L
    _disposed: bool
    _default_sender_option: SenderOption

    def __init__(self: Self, geometry: GeometryPtr, ptr: ControllerPtr, link: L, default_sender_option: SenderOption) -> None:
        super().__init__(geometry)
        self._ptr = ptr
        self._link = link
        self._link._ptr = Base().link_get(self._ptr)
        self._disposed = False
        self._default_sender_option = default_sender_option

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
        return Controller.open_with_option(devices, link, SenderOption(), SpinSleeper())

    @staticmethod
    def open_with_option(
        devices: Iterable[AUTD3],
        link: L,
        option: SenderOption,
        sleeper: StdSleeper | SpinSleeper | WaitableSleeper,
    ) -> "Controller[L]":
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
                sleeper._inner(),
            ),
        )
        geometry = Base().geometry(ptr)
        return Controller(geometry, ptr, link, option)

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

    def sender(self: Self, option: SenderOption, sleeper: SpinSleeper | StdSleeper | WaitableSleeper) -> Sender:
        return Sender(Base().sender(self._ptr, option._inner(), sleeper._inner()), self.geometry())

    def send(
        self: Self,
        d: Datagram | tuple[Datagram, Datagram],
    ) -> None:
        self.sender(self._default_sender_option, SpinSleeper()).send(d)

    @property
    def default_sender_option(self: Self) -> SenderOption:
        return self._default_sender_option

    @default_sender_option.setter
    def default_sender_option(self: Self, option: SenderOption) -> None:
        self._default_sender_option = option
        Base().set_default_sender_option(self._ptr, option._inner())
