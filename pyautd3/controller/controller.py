import asyncio
import ctypes
from collections.abc import Callable, Iterable
from datetime import timedelta
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
from pyautd3.native_methods.autd3capi import ControllerBuilderPtr, ControllerPtr, RuntimePtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr, HandlePtr, TimerStrategyWrap
from pyautd3.native_methods.structs import FfiFuture, Quaternion, Vector3
from pyautd3.native_methods.utils import _validate_ptr, _validate_status

if TYPE_CHECKING:
    from pyautd3.emulator import Emulator, Recorder

K = TypeVar("K")
L = TypeVar("L", bound=Link)


@builder
class _Builder:
    devices: list[AUTD3]
    _param_fallback_parallel_threshold: int
    _param_fallback_timeout: timedelta
    _param_send_interval: timedelta
    _param_receive_interval: timedelta
    _param_timer_strategy: TimerStrategyWrap

    def __init__(self: Self, iterable: Iterable[AUTD3]) -> None:
        self.devices = list(iterable)
        self._param_fallback_parallel_threshold = 4
        self._param_fallback_timeout = timedelta(milliseconds=20)
        self._param_send_interval = timedelta(milliseconds=1)
        self._param_receive_interval = timedelta(milliseconds=1)
        self._param_timer_strategy = TimerStrategy.Spin(SpinSleeper())

    def _ptr(self: Self) -> ControllerBuilderPtr:
        pos = np.fromiter((np.void(Vector3(d.position)) for d in self.devices), dtype=Vector3)  # type: ignore[type-var,call-overload]
        rot = np.fromiter((np.void(Quaternion(d.rotation)) for d in self.devices), dtype=Quaternion)  # type: ignore[type-var,call-overload]
        return Base().controller_builder(
            pos.ctypes.data_as(ctypes.POINTER(Vector3)),  # type: ignore[arg-type]
            rot.ctypes.data_as(ctypes.POINTER(Quaternion)),  # type: ignore[arg-type]
            len(pos),
            self._param_fallback_parallel_threshold,
            int(self._param_fallback_timeout.total_seconds() * 1000 * 1000 * 1000),
            int(self._param_send_interval.total_seconds() * 1000 * 1000 * 1000),
            int(self._param_receive_interval.total_seconds() * 1000 * 1000 * 1000),
            self._param_timer_strategy,
        )

    async def open_async(
        self: Self,
        link: LinkBuilder[L],
        *,
        timeout: timedelta | None = None,  # noqa: ASYNC109
    ) -> "Controller[L]":
        return await Controller._open_impl_async(self._ptr(), link, timeout)

    def open(self: Self, link: LinkBuilder[L], *, timeout: timedelta | None = None) -> "Controller[L]":
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

    async def send_async(self: Self) -> None:
        keys = np.array(self._keys, dtype=np.int32)
        datagrams: np.ndarray = np.ndarray(len(self._datagrams), dtype=DatagramPtr)
        for i, d in enumerate(self._datagrams):
            datagrams[i]["_0"] = d._0
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future = Base().controller_group(
            self._controller._ptr,
            self._f_native,  # type: ignore[arg-type]
            None,
            self._controller._geometry_ptr,
            keys.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),  # type: ignore[arg-type]
            datagrams.ctypes.data_as(ctypes.POINTER(DatagramPtr)),  # type: ignore[arg-type]
            len(self._keys),
        )
        loop.call_soon(
            lambda *_: future.set_result(
                Base().wait_local_result_status(self._controller._handle, ffi_future),
            ),
        )
        _validate_status(await future)

    def send(self: Self) -> None:
        keys = np.array(self._keys, dtype=np.int32)
        datagrams: np.ndarray = np.ndarray(len(self._datagrams), dtype=DatagramPtr)
        for i, d in enumerate(self._datagrams):
            datagrams[i]["_0"] = d._0
        _validate_status(
            Base().wait_local_result_status(
                self._controller._handle,
                Base().controller_group(
                    self._controller._ptr,
                    self._f_native,  # type: ignore[arg-type]
                    None,
                    self._controller._geometry_ptr,
                    keys.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),  # type: ignore[arg-type]
                    datagrams.ctypes.data_as(ctypes.POINTER(DatagramPtr)),  # type: ignore[arg-type]
                    len(self._keys),
                ),
            ),
        )


class Controller(Geometry, Generic[L]):
    _runtime: RuntimePtr
    _handle: HandlePtr
    _ptr: ControllerPtr
    _link: L
    _disposed: bool

    def __init__(self: Self, geometry: GeometryPtr, runtime: RuntimePtr, handle: HandlePtr, ptr: ControllerPtr, link: L) -> None:
        super().__init__(geometry)
        self._runtime = runtime
        self._handle = handle
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
    async def _open_impl_async(
        builder: ControllerBuilderPtr,
        link_builder: LinkBuilder[L],
        timeout: timedelta | None = None,  # noqa: ASYNC109
    ) -> "Controller[L]":
        runtime = Base().create_runtime()
        handle = Base().get_runtime_handle(runtime)
        timeout_ns = -1 if timeout is None else int(timeout.total_seconds() * 1000 * 1000 * 1000)
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future = Base().controller_open(builder, link_builder._link_builder_ptr(), timeout_ns)
        loop.call_soon(
            lambda *_: future.set_result(Base().wait_result_controller(handle, ffi_future)),
        )
        ptr = _validate_ptr(await future)
        geometry = Base().geometry(ptr)
        link = link_builder._resolve_link(handle, ptr)
        return Controller(geometry, runtime, handle, ptr, link)

    @staticmethod
    def _open_impl(
        builder: ControllerBuilderPtr,
        link_builder: LinkBuilder[L],
        timeout: timedelta | None = None,
    ) -> "Controller[L]":
        runtime = Base().create_runtime()
        handle = Base().get_runtime_handle(runtime)
        timeout_ns = -1 if timeout is None else int(timeout.total_seconds() * 1000 * 1000 * 1000)
        ptr = _validate_ptr(
            Base().wait_result_controller(
                handle,
                Base().controller_open(builder, link_builder._link_builder_ptr(), timeout_ns),
            ),
        )
        geometry = Base().geometry(ptr)
        link = link_builder._resolve_link(handle, ptr)
        return Controller(geometry, runtime, handle, ptr, link)

    async def firmware_version_async(self: Self) -> list[FirmwareInfo]:
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future = Base().controller_firmware_version_list_pointer(self._ptr)
        loop.call_soon(
            lambda *_: future.set_result(
                Base().wait_result_firmware_version_list(self._handle, ffi_future),
            ),
        )
        handle = _validate_ptr(await future)

        def get_firmware_info(i: int) -> FirmwareInfo:
            sb = ctypes.create_string_buffer(256)
            Base().controller_firmware_version_get(handle, i, sb)
            info = sb.value.decode("utf-8")
            return FirmwareInfo(info)

        res = list(map(get_firmware_info, range(self.num_devices)))
        Base().controller_firmware_version_list_pointer_delete(handle)
        return res

    def firmware_version(self: Self) -> list[FirmwareInfo]:
        handle = _validate_ptr(
            Base().wait_result_firmware_version_list(
                self._handle,
                Base().controller_firmware_version_list_pointer(self._ptr),
            ),
        )

        def get_firmware_info(i: int) -> FirmwareInfo:
            sb = ctypes.create_string_buffer(256)
            Base().controller_firmware_version_get(handle, i, sb)
            info = sb.value.decode("utf-8")
            return FirmwareInfo(info)

        res = list(map(get_firmware_info, range(self.num_devices)))
        Base().controller_firmware_version_list_pointer_delete(handle)
        return res

    async def close_async(self: Self) -> None:
        if self._disposed:
            return
        self._disposed = True
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future = Base().controller_close(self._ptr)
        loop.call_soon(
            lambda *_: future.set_result(
                Base().wait_result_status(self._handle, ffi_future),
            ),
        )
        r = await future
        Base().delete_runtime(self._runtime)
        self._ptr._0 = None
        self._runtime._0 = None
        self._handle._0 = None
        _validate_status(r)

    def close(self: Self) -> None:
        if self._disposed:
            return
        self._disposed = True
        r = Base().wait_result_status(self._handle, Base().controller_close(self._ptr))
        Base().delete_runtime(self._runtime)
        self._ptr._0 = None
        self._runtime._0 = None
        self._handle._0 = None
        _validate_status(r)

    async def fpga_state_async(self: Self) -> list[FPGAState | None]:
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future = Base().controller_fpga_state(self._ptr)
        loop.call_soon(
            lambda *_: future.set_result(Base().wait_result_fpga_state_list(self._handle, ffi_future)),
        )
        handle = _validate_ptr(await future)

        def get_fpga_state(i: int) -> FPGAState | None:
            state = int(Base().controller_fpga_state_get(handle, i))
            return None if state == -1 else FPGAState(state)

        res = list(map(get_fpga_state, range(self.num_devices)))
        Base().controller_fpga_state_delete(handle)
        return res

    def fpga_state(self: Self) -> list[FPGAState | None]:
        handle = _validate_ptr(
            Base().wait_result_fpga_state_list(
                self._handle,
                Base().controller_fpga_state(self._ptr),
            ),
        )

        def get_fpga_state(i: int) -> FPGAState | None:
            state = int(Base().controller_fpga_state_get(handle, i))
            return None if state == -1 else FPGAState(state)

        res = list(map(get_fpga_state, range(self.num_devices)))
        Base().controller_fpga_state_delete(handle)
        return res

    async def send_async(
        self: Self,
        d: Datagram | tuple[Datagram, Datagram],
    ) -> None:
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future: FfiFuture
        match d:
            case Datagram():
                ffi_future = Base().controller_send(self._ptr, d._datagram_ptr(self.geometry))
            case (Datagram(), Datagram()):
                (d1, d2) = d
                d_tuple = Base().datagram_tuple(d1._datagram_ptr(self.geometry), d2._datagram_ptr(self.geometry))
                ffi_future = Base().controller_send(self._ptr, d_tuple)
            case _:
                raise InvalidDatagramTypeError
        loop.call_soon(
            lambda *_: future.set_result(Base().wait_result_status(self._handle, ffi_future)),
        )
        _validate_status(await future)

    def send(
        self: Self,
        d: Datagram | tuple[Datagram, Datagram],
    ) -> None:
        ffi_future: FfiFuture
        match d:
            case Datagram():
                ffi_future = Base().controller_send(self._ptr, d._datagram_ptr(self.geometry))
            case (Datagram(), Datagram()):
                (d1, d2) = d
                d_tuple = Base().datagram_tuple(d1._datagram_ptr(self.geometry), d2._datagram_ptr(self.geometry))
                ffi_future = Base().controller_send(self._ptr, d_tuple)
            case _:
                raise InvalidDatagramTypeError
        _validate_status(Base().wait_result_status(self._handle, ffi_future))

    def group(self: Self, group_map: Callable[[Device], K | None]) -> _GroupGuard:
        return _GroupGuard(group_map, self)

    def tick(self: "Controller[Recorder]", tick: timedelta) -> None:
        raise NotImplementedError  # pragma: no cover
