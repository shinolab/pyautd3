import ctypes
from collections.abc import Callable, Iterable
from types import TracebackType
from typing import TYPE_CHECKING, Generic, Self, TypeVar

import numpy as np

from pyautd3.autd_error import InvalidDatagramTypeError, KeyAlreadyExistsError
from pyautd3.controller.timer import SpinSleeper, TimerStrategy
from pyautd3.derive import builder
from pyautd3.driver.autd3_device import AUTD3
from pyautd3.driver.datagram import Datagram
from pyautd3.driver.firmware.fpga import FPGAState
from pyautd3.driver.firmware_version import FirmwareInfo
from pyautd3.driver.geometry import Device, Geometry
from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerBuilderPtr, ControllerPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr, TimerStrategyWrap
from pyautd3.native_methods.structs import Point3, Quaternion
from pyautd3.native_methods.utils import _validate_ptr, _validate_status
from pyautd3.utils import Duration
from pyautd3.utils.duration import into_option_duration

if TYPE_CHECKING:
    from pyautd3.emulator import Emulator, Recorder

K = TypeVar("K")
L = TypeVar("L", bound=Link)


@builder
class _Builder:
    devices: list[AUTD3]
    _param_default_parallel_threshold: int
    _param_default_timeout: Duration
    _param_send_interval: Duration
    _param_receive_interval: Duration
    _param_timer_strategy: TimerStrategyWrap

    def __init__(self: Self, iterable: Iterable[AUTD3]) -> None:
        self.devices = list(iterable)
        self._param_default_parallel_threshold = 4
        self._param_default_timeout = Duration.from_millis(20)
        self._param_send_interval = Duration.from_millis(1)
        self._param_receive_interval = Duration.from_millis(1)
        self._param_timer_strategy = TimerStrategy.Spin(SpinSleeper())

    def _ptr(self: Self) -> ControllerBuilderPtr:
        pos = np.fromiter((np.void(Point3(d.position)) for d in self.devices), dtype=Point3)  # type: ignore[type-var,call-overload]
        rot = np.fromiter((np.void(Quaternion(d.rotation)) for d in self.devices), dtype=Quaternion)  # type: ignore[type-var,call-overload]
        return Base().controller_builder(
            pos.ctypes.data_as(ctypes.POINTER(Point3)),  # type: ignore[arg-type]
            rot.ctypes.data_as(ctypes.POINTER(Quaternion)),  # type: ignore[arg-type]
            len(pos),
            self._param_default_parallel_threshold,
            self._param_default_timeout._inner,
            self._param_send_interval._inner,
            self._param_receive_interval._inner,
            self._param_timer_strategy,
        )

    def open(self: Self, link: LinkBuilder[L], *, timeout: Duration | None = None) -> "Controller[L]":
        return Controller._open_impl(self._ptr(), link, timeout)

    def into_emulator(self: Self) -> "Emulator":  # type: ignore[empty-body]
        pass  # pragma: no cover


class _GroupGuard(Generic[K]):
    _controller: "Controller"
    _keys: list[int]
    _datagrams: list[DatagramPtr]
    _keymap: dict[K, int]
    _k: int

    def __init__(self: Self, group_map: Callable[[Device], K | None], controller: "Controller") -> None:
        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int) -> int:
            dev = Device(dev_idx, geometry_ptr)
            key = group_map(dev)
            return self._keymap[key] if key is not None else -1

        self._f_native = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, GeometryPtr, ctypes.c_uint16)(f_native)
        self._controller = controller
        self._keys = []
        self._datagrams = []
        self._keymap = {}
        self._k = 0

    def set(
        self: Self,
        key: K,
        d: Datagram | tuple[Datagram, Datagram],
    ) -> "_GroupGuard[K]":
        if key in self._keymap:
            raise KeyAlreadyExistsError
        match d:
            case Datagram():
                ptr = d._datagram_ptr(self._controller.geometry)
                self._datagrams.append(ptr)
            case (Datagram(), Datagram()):
                (d1, d2) = d
                ptr = Base().datagram_tuple(
                    d1._datagram_ptr(self._controller.geometry),
                    d2._datagram_ptr(self._controller.geometry),
                )
                self._datagrams.append(ptr)
            case _:
                raise InvalidDatagramTypeError
        self._keys.append(self._k)
        self._keymap[key] = self._k
        self._k += 1

        return self

    def send(self: Self) -> None:
        keys = np.array(self._keys, dtype=np.int32)
        datagrams: np.ndarray = np.ndarray(len(self._datagrams), dtype=DatagramPtr)
        for i, d in enumerate(self._datagrams):
            datagrams[i]["_0"] = d._0
        _validate_status(
            Base().controller_group(
                self._controller._ptr,
                self._f_native,  # type: ignore[arg-type]
                None,
                self._controller._geometry_ptr,
                keys.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),  # type: ignore[arg-type]
                datagrams.ctypes.data_as(ctypes.POINTER(DatagramPtr)),  # type: ignore[arg-type]
                len(self._keys),
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
        self._disposed = False

    @property
    def link(self: Self) -> L:
        return self._link

    @staticmethod
    def builder(iterable: Iterable[AUTD3]) -> _Builder:
        return _Builder(iterable)

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

    @property
    def geometry(self: Self) -> Geometry:
        return self  # type: ignore[return-value]

    @staticmethod
    def _open_impl(
        builder: ControllerBuilderPtr,
        link_builder: LinkBuilder[L],
        timeout: Duration | None = None,
    ) -> "Controller[L]":
        ptr = _validate_ptr(
            Base().controller_open(builder, link_builder._link_builder_ptr(), into_option_duration(timeout)),
        )
        geometry = Base().geometry(ptr)
        link = link_builder._resolve_link(ptr)
        return Controller(geometry, ptr, link)

    def firmware_version(self: Self) -> list[FirmwareInfo]:
        handle = _validate_ptr(
            Base().controller_firmware_version_list_pointer(self._ptr),
        )

        def get_firmware_info(i: int) -> FirmwareInfo:
            sb = ctypes.create_string_buffer(256)
            Base().controller_firmware_version_get(handle, i, sb)
            info = sb.value.decode("utf-8")
            return FirmwareInfo(info)

        res = list(map(get_firmware_info, range(self.num_devices)))
        Base().controller_firmware_version_list_pointer_delete(handle)
        return res

    def close(self: Self) -> None:
        if self._disposed:
            return
        self._disposed = True
        r = Base().controller_close(self._ptr)
        self._ptr._0 = None
        _validate_status(r)

    def fpga_state(self: Self) -> list[FPGAState | None]:
        handle = _validate_ptr(Base().controller_fpga_state(self._ptr))

        def get_fpga_state(i: int) -> FPGAState | None:
            state = int(Base().controller_fpga_state_get(handle, i))
            return None if state == -1 else FPGAState(state)

        res = list(map(get_fpga_state, range(self.num_devices)))
        Base().controller_fpga_state_delete(handle)
        return res

    def send(
        self: Self,
        d: Datagram | tuple[Datagram, Datagram],
    ) -> None:
        match d:
            case Datagram():
                result = Base().controller_send(self._ptr, d._datagram_ptr(self.geometry))
            case (Datagram(), Datagram()):
                (d1, d2) = d
                d_tuple = Base().datagram_tuple(d1._datagram_ptr(self.geometry), d2._datagram_ptr(self.geometry))
                result = Base().controller_send(self._ptr, d_tuple)
            case _:
                raise InvalidDatagramTypeError
        _validate_status(result)

    def group(self: Self, group_map: Callable[[Device], K | None]) -> _GroupGuard:
        return _GroupGuard(group_map, self)

    def tick(self: "Controller[Recorder]", tick: Duration) -> None:
        raise NotImplementedError  # pragma: no cover
