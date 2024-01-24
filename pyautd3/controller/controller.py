import asyncio
import ctypes
from collections.abc import Callable
from datetime import timedelta
from types import TracebackType
from typing import Generic, TypeVar

import numpy as np

from pyautd3.autd_error import InvalidDatagramTypeError, KeyAlreadyExistsError
from pyautd3.driver.autd3_device import AUTD3
from pyautd3.driver.datagram import Datagram
from pyautd3.driver.firmware_version import FirmwareInfo
from pyautd3.driver.fpga.defined.fpga_state import FPGAState
from pyautd3.driver.geometry import Device, Geometry
from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerBuilderPtr, GroupKVMapPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import (
    AUTD3_TRUE,
    ControllerPtr,
    DatagramPtr,
)
from pyautd3.native_methods.utils import _validate_int, _validate_ptr

K = TypeVar("K")
L = TypeVar("L", bound=Link)


class _Builder(Generic[L]):
    _ptr: ControllerBuilderPtr

    def __init__(self: "_Builder[L]") -> None:
        self._ptr = Base().controller_builder()

    def add_device(self: "_Builder[L]", device: AUTD3) -> "_Builder[L]":
        """Add device.

        Arguments:
        ---------
            device: Device to add
        """
        q = device._rot if device._rot is not None else np.array([1.0, 0.0, 0.0, 0.0])
        self._ptr = Base().controller_builder_add_device(
            self._ptr,
            device._pos[0],
            device._pos[1],
            device._pos[2],
            q[0],
            q[1],
            q[2],
            q[3],
        )
        return self

    async def open_with_async(self: "_Builder[L]", link: LinkBuilder[L]) -> "Controller[L]":
        """Open controller.

        Arguments:
        ---------
            link: LinkBuilder
        """
        return await Controller._open_impl_async(self._ptr, link)

    def open_with(self: "_Builder[L]", link: LinkBuilder[L]) -> "Controller[L]":
        """Open controller.

        Arguments:
        ---------
            link: LinkBuilder
        """
        return Controller._open_impl(self._ptr, link)


class _GroupGuard(Generic[K]):
    _controller: "Controller"
    _map: Callable[[Device], K | None]
    _kv_map: GroupKVMapPtr
    _keymap: dict[K, int]
    _k: int

    def __init__(self: "_GroupGuard", group_map: Callable[[Device], K | None], controller: "Controller") -> None:
        self._map = group_map
        self._controller = controller
        self._kv_map = Base().controller_group_create_kv_map()
        self._keymap = {}
        self._k = 0

    def set_data(
        self: "_GroupGuard",
        key: K,
        d1: Datagram | tuple[Datagram, Datagram],
        d2: Datagram | None = None,
        *,
        timeout: timedelta | None = None,
    ) -> "_GroupGuard":
        if key in self._keymap:
            raise KeyAlreadyExistsError
        self._keymap[key] = self._k

        timeout_ns = -1 if timeout is None else int(timeout.total_seconds() * 1000 * 1000 * 1000)

        match (d1, d2):
            case (Datagram(), None):
                self._kv_map = _validate_ptr(
                    Base().controller_group_kv_map_set(
                        self._kv_map,
                        self._k,
                        d1._datagram_ptr(self._controller._geometry),  # type: ignore[union-attr]
                        DatagramPtr(None),
                        timeout_ns,
                    ),
                )
            case ((Datagram(), Datagram()), None):
                (d11, d12) = d1  # type: ignore[misc]
                self._kv_map = _validate_ptr(
                    Base().controller_group_kv_map_set(
                        self._kv_map,
                        self._k,
                        d11._datagram_ptr(self._controller._geometry),  # type: ignore[union-attr]
                        d12._datagram_ptr(self._controller._geometry),  # type: ignore[union-attr]
                        timeout_ns,
                    ),
                )
            case (Datagram(), Datagram()):
                self._kv_map = _validate_ptr(
                    Base().controller_group_kv_map_set(
                        self._kv_map,
                        self._k,
                        d1._datagram_ptr(self._controller._geometry),  # type: ignore[union-attr]
                        d2._datagram_ptr(self._controller._geometry),  # type: ignore[union-attr]
                        timeout_ns,
                    ),
                )
            case _:
                raise InvalidDatagramTypeError

        self._k += 1

        return self

    async def send_async(self: "_GroupGuard") -> bool:
        m = np.fromiter(
            (self._keymap[k] if k is not None else -1 for k in (self._map(dev) if dev.enable else None for dev in self._controller.geometry)),
            dtype=np.int32,
        )
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        loop.call_soon(
            lambda *_: future.set_result(
                Base().controller_group(
                    self._controller._ptr,
                    np.ctypeslib.as_ctypes(m.astype(ctypes.c_int32)),
                    self._kv_map,
                ),
            ),
        )
        return _validate_int(await future) == AUTD3_TRUE

    def send(self: "_GroupGuard") -> bool:
        m = np.fromiter(
            (self._keymap[k] if k is not None else -1 for k in (self._map(dev) if dev.enable else None for dev in self._controller.geometry)),
            dtype=np.int32,
        )
        return (
            _validate_int(
                Base().controller_group(
                    self._controller._ptr,
                    np.ctypeslib.as_ctypes(m.astype(ctypes.c_int32)),
                    self._kv_map,
                ),
            )
            == AUTD3_TRUE
        )


class Controller(Generic[L]):
    """Controller."""

    _geometry: Geometry
    _ptr: ControllerPtr
    link: L

    def __init__(self: "Controller", geometry: Geometry, ptr: ControllerPtr, link: L) -> None:
        self._geometry = geometry
        self._ptr = ptr
        self.link = link

    @staticmethod
    def builder() -> "_Builder[L]":
        """Create builder."""
        return _Builder()

    def __del__(self: "Controller") -> None:
        self._dispose()

    def _dispose(self: "Controller") -> None:
        if self._ptr._0 is not None:
            Base().controller_delete(self._ptr)
            self._ptr._0 = None

    def __enter__(self: "Controller") -> "Controller":
        return self

    def __exit__(
        self: "Controller",
        _exc_type: type[BaseException] | None,
        _exc_value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        self._dispose()

    @property
    def geometry(self: "Controller") -> Geometry:
        """Get geometry."""
        return self._geometry

    @staticmethod
    async def _open_impl_async(builder: ControllerBuilderPtr, link_builder: LinkBuilder[L]) -> "Controller[L]":
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        loop.call_soon(
            lambda *_: future.set_result(
                Base().controller_open_with(
                    builder,
                    link_builder._link_builder_ptr(),
                ),
            ),
        )
        ptr = _validate_ptr(await future)
        geometry = Geometry(Base().geometry(ptr))
        link = link_builder._resolve_link(ptr)
        return Controller(geometry, ptr, link)

    @staticmethod
    def _open_impl(builder: ControllerBuilderPtr, link_builder: LinkBuilder[L]) -> "Controller[L]":
        ptr = _validate_ptr(
            Base().controller_open_with(
                builder,
                link_builder._link_builder_ptr(),
            ),
        )
        geometry = Geometry(Base().geometry(ptr))
        link = link_builder._resolve_link(ptr)
        return Controller(geometry, ptr, link)

    async def firmware_info_list_async(self: "Controller") -> list[FirmwareInfo]:
        """Get firmware information list."""
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        loop.call_soon(
            lambda *_: future.set_result(Base().controller_firmware_info_list_pointer(self._ptr)),
        )
        handle = _validate_ptr(await future)

        def get_firmware_info(i: int) -> FirmwareInfo:
            sb = ctypes.create_string_buffer(256)
            Base().controller_firmware_info_get(handle, i, sb)
            info = sb.value.decode("utf-8")
            return FirmwareInfo(info)

        res = list(map(get_firmware_info, range(self.geometry.num_devices)))
        Base().controller_firmware_info_list_pointer_delete(handle)
        return res

    def firmware_info_list(self: "Controller") -> list[FirmwareInfo]:
        """Get firmware information list."""
        handle = _validate_ptr(Base().controller_firmware_info_list_pointer(self._ptr))

        def get_firmware_info(i: int) -> FirmwareInfo:
            sb = ctypes.create_string_buffer(256)
            Base().controller_firmware_info_get(handle, i, sb)
            info = sb.value.decode("utf-8")
            return FirmwareInfo(info)

        res = list(map(get_firmware_info, range(self.geometry.num_devices)))
        Base().controller_firmware_info_list_pointer_delete(handle)
        return res

    async def close_async(self: "Controller") -> bool:
        """Close controller."""
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        loop.call_soon(
            lambda *_: future.set_result(
                Base().controller_close(self._ptr),
            ),
        )
        return _validate_int(await future) == AUTD3_TRUE

    def close(self: "Controller") -> bool:
        """Close controller."""
        return _validate_int(Base().controller_close(self._ptr)) == AUTD3_TRUE

    async def fpga_state_async(self: "Controller") -> list[FPGAState | None]:
        """Get FPGA information list."""
        infos = np.zeros([self.geometry.num_devices]).astype(ctypes.c_int32)
        pinfos = np.ctypeslib.as_ctypes(infos)
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        loop.call_soon(
            lambda *_: future.set_result(Base().controller_fpga_state(self._ptr, pinfos)),
        )
        _validate_int(await future)
        return [None if x == -1 else FPGAState(x) for x in infos]

    def fpga_state(self: "Controller") -> list[FPGAState | None]:
        """Get FPGA information list."""
        infos = np.zeros([self.geometry.num_devices]).astype(ctypes.c_int32)
        pinfos = np.ctypeslib.as_ctypes(infos)
        _validate_int(Base().controller_fpga_state(self._ptr, pinfos))
        return [None if x == -1 else FPGAState(x) for x in infos]

    async def send_async(
        self: "Controller",
        d1: Datagram | tuple[Datagram, Datagram],
        d2: Datagram | None = None,
        *,
        timeout: timedelta | None = None,
    ) -> bool:
        """Send data.

        Arguments:
        ---------
            d1: Data to send
            d2: Data to send
            timeout: Timeout

        Returns:
        -------
            bool: If true, it is confirmed that the data has been successfully transmitted.
                  If false, there are no errors, but it is unclear whether the data has been sent reliably or not.

        Raises:
        ------
            AUTDError: If an error occurs
        """
        timeout_ = -1 if timeout is None else int(timeout.total_seconds() * 1000 * 1000 * 1000)
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        match (d1, d2):
            case (Datagram(), None):
                d_ptr: DatagramPtr = d1._datagram_ptr(self.geometry)  # type: ignore[union-attr]
                loop.call_soon(
                    lambda *_: future.set_result(
                        Base().controller_send(
                            self._ptr,
                            d_ptr,
                            DatagramPtr(None),
                            timeout_,
                        ),
                    ),
                )
            case ((Datagram(), Datagram()), None):
                (d11, d12) = d1  # type: ignore[misc]
                d11_ptr: DatagramPtr = d11._datagram_ptr(self.geometry)
                d22_ptr: DatagramPtr = d12._datagram_ptr(self.geometry)
                loop.call_soon(
                    lambda *_: future.set_result(
                        Base().controller_send(
                            self._ptr,
                            d11_ptr,
                            d22_ptr,
                            timeout_,
                        ),
                    ),
                )
            case (Datagram(), Datagram()):
                d1_ptr: DatagramPtr = d1._datagram_ptr(self.geometry)  # type: ignore[union-attr]
                d2_ptr: DatagramPtr = d2._datagram_ptr(self.geometry)  # type: ignore[union-attr]
                loop.call_soon(
                    lambda *_: future.set_result(
                        Base().controller_send(
                            self._ptr,
                            d1_ptr,
                            d2_ptr,
                            timeout_,
                        ),
                    ),
                )
            case _:
                raise InvalidDatagramTypeError
        res = _validate_int(await future)
        return res == AUTD3_TRUE

    def send(
        self: "Controller",
        d1: Datagram | tuple[Datagram, Datagram],
        d2: Datagram | None = None,
        *,
        timeout: timedelta | None = None,
    ) -> bool:
        """Send data.

        Arguments:
        ---------
            d1: Data to send
            d2: Data to send
            timeout: Timeout

        Returns:
        -------
            bool: If true, it is confirmed that the data has been successfully transmitted.
                  If false, there are no errors, but it is unclear whether the data has been sent reliably or not.

        Raises:
        ------
            AUTDError: If an error occurs
        """
        timeout_ = -1 if timeout is None else int(timeout.total_seconds() * 1000 * 1000 * 1000)
        res: int
        match (d1, d2):
            case (Datagram(), None):
                d_ptr: DatagramPtr = d1._datagram_ptr(self.geometry)  # type: ignore[union-attr]
                res = _validate_int(
                    Base().controller_send(
                        self._ptr,
                        d_ptr,
                        DatagramPtr(None),
                        timeout_,
                    ),
                )
            case ((Datagram(), Datagram()), None):
                (d11, d12) = d1  # type: ignore[misc]
                d11_ptr: DatagramPtr = d11._datagram_ptr(self.geometry)
                d22_ptr: DatagramPtr = d12._datagram_ptr(self.geometry)
                res = _validate_int(
                    Base().controller_send(
                        self._ptr,
                        d11_ptr,
                        d22_ptr,
                        timeout_,
                    ),
                )
            case (Datagram(), Datagram()):
                d1_ptr: DatagramPtr = d1._datagram_ptr(self.geometry)  # type: ignore[union-attr]
                d2_ptr: DatagramPtr = d2._datagram_ptr(self.geometry)  # type: ignore[union-attr]
                res = _validate_int(
                    Base().controller_send(
                        self._ptr,
                        d1_ptr,
                        d2_ptr,
                        timeout_,
                    ),
                )
            case _:
                raise InvalidDatagramTypeError
        return res == AUTD3_TRUE

    def group(self: "Controller", group_map: Callable[[Device], K | None]) -> _GroupGuard:
        """Grouping data."""
        return _GroupGuard(group_map, self)
