import asyncio
import ctypes
from collections.abc import Callable
from datetime import timedelta
from types import TracebackType
from typing import Self

import numpy as np
import polars as pl

from pyautd3.controller.controller import Controller, _Builder
from pyautd3.driver.geometry.geometry import Geometry
from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi import ControllerPtr, RuntimePtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GeometryPtr, HandlePtr, LinkPtr
from pyautd3.native_methods.autd3capi_emulator import EmulatorPtr, RecordPtr, SoundFieldPtr
from pyautd3.native_methods.autd3capi_emulator import NativeMethods as Emu
from pyautd3.native_methods.autd3capi_emulator import Range as Range_
from pyautd3.native_methods.autd3capi_emulator import RecordOption as RecordOption_
from pyautd3.native_methods.utils import _validate_ptr, _validate_status


class Range:
    _inner: Range_

    def __init__(
        self: Self,
        *,
        x_start: float,
        x_end: float,
        y_start: float,
        y_end: float,
        z_start: float,
        z_end: float,
        resolution: float,
    ) -> None:
        self._inner = Range_(
            x_start,
            x_end,
            y_start,
            y_end,
            z_start,
            z_end,
            resolution,
        )


class RecordOption:
    _inner: RecordOption_

    def __init__(
        self: Self,
        *,
        sound_speed: float | None = None,
        time_step_ns: int | None = None,
        print_progress: bool | None = None,
        memory_limits_hint_mb: int | None = None,
        gpu: bool | None = None,
    ) -> None:
        self._inner = RecordOption_(
            sound_speed if sound_speed is not None else 340e3,
            time_step_ns if time_step_ns is not None else 1000,
            print_progress if print_progress is not None else False,
            memory_limits_hint_mb if memory_limits_hint_mb is not None else 128,
            gpu if gpu is not None else False,
        )


class SoundField:
    _ptr: SoundFieldPtr
    _handle: HandlePtr

    def __init__(self: Self, ptr: SoundFieldPtr, handle: HandlePtr) -> None:
        self._ptr = ptr
        self._handle = handle

    def __del__(self: Self) -> None:
        self._dispose()

    def _dispose(self: Self) -> None:
        if self._ptr._0 is not None:  # pragma: no cover
            Emu().emulator_sound_field_free(self._ptr)
            self._ptr._0 = None

    def skip(self: Self, duration: timedelta) -> Self:
        _validate_status(
            Base().wait_local_result_status(
                self._handle,
                Emu().emulator_sound_field_skip(self._ptr, int(duration.total_seconds() * 1000 * 1000 * 1000)),
            ),
        )
        return self

    def next(self: Self, duration: timedelta) -> pl.DataFrame:
        n = int(Emu().emulator_sound_field_time_len(self._ptr, int(duration.total_seconds() * 1000 * 1000 * 1000)))
        points_len = int(Emu().emulator_sound_field_points_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)

        x = np.zeros(points_len, dtype=np.float32)
        y = np.zeros(points_len, dtype=np.float32)
        z = np.zeros(points_len, dtype=np.float32)
        Emu().emulator_sound_field_get_x(self._ptr, x.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_get_y(self._ptr, y.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_get_z(self._ptr, z.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]

        v = np.zeros([n, points_len], dtype=np.float32)
        _validate_status(
            Base().wait_local_result_status(
                self._handle,
                Emu().emulator_sound_field_next(
                    self._ptr,
                    int(duration.total_seconds() * 1000 * 1000 * 1000),
                    time.ctypes.data_as(ctypes.POINTER(ctypes.c_ulonglong)),  # type: ignore[arg-type]
                    ctypes.cast(
                        (ctypes.POINTER(ctypes.c_float) * n)(
                            *(ctypes.cast(r, ctypes.POINTER(ctypes.c_float)) for r in np.ctypeslib.as_ctypes(v)),  # type: ignore[arg-type]
                        ),
                        ctypes.POINTER(ctypes.POINTER(ctypes.c_float)),
                    ),  # type: ignore[arg-type]
                ),
            ),
        )
        return pl.DataFrame(
            {
                "x[mm]": x,
                "y[mm]": y,
                "z[mm]": z,
                **{s.name: s for s in (pl.Series(name=f"p[Pa]@{time[i]}[ns]", values=v[i]) for i in range(n))},
            },
        )

    async def next_async(self: Self, duration: timedelta) -> pl.DataFrame:
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()

        n = int(Emu().emulator_sound_field_time_len(self._ptr, int(duration.total_seconds() * 1000 * 1000 * 1000)))
        points_len = int(Emu().emulator_sound_field_points_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)

        x = np.zeros(points_len, dtype=np.float32)
        y = np.zeros(points_len, dtype=np.float32)
        z = np.zeros(points_len, dtype=np.float32)
        Emu().emulator_sound_field_get_x(self._ptr, x.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_get_y(self._ptr, y.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_get_z(self._ptr, z.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]

        v = np.zeros([n, points_len], dtype=np.float32)
        ffi_future = Emu().emulator_sound_field_next(
            self._ptr,
            int(duration.total_seconds() * 1000 * 1000 * 1000),
            time.ctypes.data_as(ctypes.POINTER(ctypes.c_ulonglong)),  # type: ignore[arg-type]
            ctypes.cast(
                (ctypes.POINTER(ctypes.c_float) * n)(
                    *(ctypes.cast(r, ctypes.POINTER(ctypes.c_float)) for r in np.ctypeslib.as_ctypes(v)),  # type: ignore[arg-type]
                ),
                ctypes.POINTER(ctypes.POINTER(ctypes.c_float)),
            ),  # type: ignore[arg-type]
        )
        loop.call_soon(
            lambda *_: future.set_result(
                Base().wait_local_result_status(
                    self._handle,
                    ffi_future,
                ),
            ),
        )
        _validate_status(await future)
        return pl.DataFrame(
            {
                "x[mm]": x,
                "y[mm]": y,
                "z[mm]": z,
                **{s.name: s for s in (pl.Series(name=f"p[Pa]@{time[i]}[ns]", values=v[i]) for i in range(n))},
            },
        )


class Recorder(Link):
    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)

    def tick(self: Self, tick: timedelta) -> None:
        _validate_status(
            Emu().emulator_tick_ns(self._ptr, int(tick.total_seconds() * 1000 * 1000 * 1000)),
        )


Controller[Recorder].tick = lambda self, tick: self._link.tick(tick)  # type: ignore[attr-defined,method-assign]


class Record:
    _ptr: RecordPtr
    _handle: HandlePtr

    def __init__(self: Self, ptr: RecordPtr, handle: HandlePtr) -> None:
        self._ptr = ptr
        self._handle = handle

    def __del__(self: Self) -> None:
        self._dispose()

    def _dispose(self: Self) -> None:
        if self._ptr._0 is not None:  # pragma: no cover
            Emu().emulator_record_free(self._ptr)
            self._ptr._0 = None

    def drive(self: Self) -> pl.DataFrame:
        n = int(Emu().emulator_record_drive_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)
        Emu().emulator_record_drive_time(
            self._ptr,
            time.ctypes.data_as(ctypes.POINTER(ctypes.c_ulonglong)),  # type: ignore[arg-type]
        )
        dev_num = int(Emu().emulator_record_num_devices(self._ptr))
        pulsewidth = np.zeros(n, dtype=np.uint8)
        phase = np.zeros(n, dtype=np.uint8)

        num_cols = sum(2 * int(Emu().emulator_record_num_transducers(self._ptr, dev_idx)) for dev_idx in range(dev_num))
        series = np.zeros([num_cols], dtype=pl.Series)
        i = 0
        for dev_idx in range(dev_num):
            for tr_idx in range(int(Emu().emulator_record_num_transducers(self._ptr, dev_idx))):
                Emu().emulator_record_drive_phase(
                    self._ptr,
                    dev_idx,
                    tr_idx,
                    phase.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                )
                Emu().emulator_record_drive_pulse_width(
                    self._ptr,
                    dev_idx,
                    tr_idx,
                    pulsewidth.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                )
                series[i] = pl.Series(name=f"phase_{dev_idx}_{tr_idx}", values=phase)
                series[i + 1] = pl.Series(name=f"pulsewidth_{dev_idx}_{tr_idx}", values=pulsewidth)
                i += 2

        return pl.DataFrame(
            {
                "time[ns]": time,
                **{s.name: s for s in series},
            },
        )

    def output_voltage(self: Self) -> pl.DataFrame:
        n = int(Emu().emulator_record_output_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)
        Emu().emulator_record_output_time(
            self._ptr,
            time.ctypes.data_as(ctypes.POINTER(ctypes.c_ulonglong)),  # type: ignore[arg-type]
        )
        dev_num = int(Emu().emulator_record_num_devices(self._ptr))
        v = np.zeros(n, dtype=np.float32)

        num_cols = sum(int(Emu().emulator_record_num_transducers(self._ptr, dev_idx)) for dev_idx in range(dev_num))
        series = np.zeros([num_cols], dtype=pl.Series)
        i = 0
        for dev_idx in range(dev_num):
            for tr_idx in range(int(Emu().emulator_record_num_transducers(self._ptr, dev_idx))):
                Emu().emulator_record_output_voltage(
                    self._ptr,
                    dev_idx,
                    tr_idx,
                    v.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                )
                series[i] = pl.Series(name=f"voltage_{dev_idx}_{tr_idx}[V]", values=v)
                i += 1

        return pl.DataFrame(
            {
                "time[25us/256]": time,
                **{s.name: s for s in series},
            },
        )

    def output_ultrasound(self: Self) -> pl.DataFrame:
        n = int(Emu().emulator_record_output_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)
        Emu().emulator_record_output_time(
            self._ptr,
            time.ctypes.data_as(ctypes.POINTER(ctypes.c_ulonglong)),  # type: ignore[arg-type]
        )
        dev_num = int(Emu().emulator_record_num_devices(self._ptr))
        v = np.zeros(n, dtype=np.float32)

        num_cols = sum(int(Emu().emulator_record_num_transducers(self._ptr, dev_idx)) for dev_idx in range(dev_num))
        series = np.zeros([num_cols], dtype=pl.Series)
        i = 0
        for dev_idx in range(dev_num):
            for tr_idx in range(int(Emu().emulator_record_num_transducers(self._ptr, dev_idx))):
                Emu().emulator_record_output_ultrasound(
                    self._ptr,
                    dev_idx,
                    tr_idx,
                    v.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                )
                series[i] = pl.Series(name=f"p_{dev_idx}_{tr_idx}[a.u.]", values=v)
                i += 1

        return pl.DataFrame(
            {
                "time[25us/256]": time,
                **{s.name: s for s in series},
            },
        )

    def sound_field(self: Self, range_: Range, option: RecordOption) -> SoundField:
        return SoundField(
            _validate_ptr(
                Emu().emulator_wait_sound_field(
                    self._handle,
                    Emu().emulator_sound_field(self._ptr, range_._inner, option._inner),
                ),
            ),
            self._handle,
        )

    async def sound_field_async(self: Self, range_: Range, option: RecordOption) -> SoundField:
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future = Emu().emulator_sound_field(self._ptr, range_._inner, option._inner)
        loop.call_soon(
            lambda *_: future.set_result(Emu().emulator_wait_sound_field(self._handle, ffi_future)),
        )
        return SoundField(
            _validate_ptr(await future),
            self._handle,
        )


class Emulator(Geometry):
    _ptr: EmulatorPtr
    _runtime: RuntimePtr
    _handle: HandlePtr

    def __new__(cls: type["Emulator"]) -> "Emulator":
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def __private_new__(cls: type["Emulator"], builder: _Builder) -> "Emulator":
        ptr = Emu().emulator(builder._ptr())
        geometry_ptr = Emu().emulator_geometry(ptr)
        ins = super().__new__(cls)
        ins._ptr = Emu().emulator(builder._ptr())
        ins._runtime = Base().create_runtime()
        ins._handle = Base().get_runtime_handle(ins._runtime)
        ins.__private_init__(geometry_ptr)
        return ins

    def __private_init__(self: Self, geometry_ptr: GeometryPtr) -> None:
        super().__init__(geometry_ptr)

    @property
    def geometry(self: Self) -> Geometry:
        return self

    def record(self: Self, f: Callable[[Controller[Recorder]], Controller[Recorder]]) -> Record:
        return self.record_from(timedelta(seconds=0), f)

    async def record_async(self: Self, f: Callable[[Controller[Recorder]], Controller[Recorder]]) -> Record:
        return await self.record_from_async(timedelta(seconds=0), f)

    def record_from(self: Self, t: timedelta, f: Callable[[Controller[Recorder]], Controller[Recorder]]) -> Record:
        def f_native(ptr: ControllerPtr) -> None:
            geometry = Base().geometry(ptr)
            link = Base().link_get(ptr)
            cnt = Controller(geometry, self._runtime, self._handle, ptr, Recorder(self._handle, link))
            cnt = f(cnt)
            cnt._disposed = True

        f_native_ = ctypes.CFUNCTYPE(None, ControllerPtr)(f_native)

        return Record(
            _validate_ptr(
                Emu().emulator_wait_result_record(
                    self._handle,
                    Emu().emulator_record_from(
                        self._ptr,
                        int(t.total_seconds() * 1000 * 1000 * 1000),
                        f_native_,  # type: ignore[arg-type]
                    ),
                ),
            ),
            self._handle,
        )

    async def record_from_async(self: Self, t: timedelta, f: Callable[[Controller[Recorder]], Controller[Recorder]]) -> Record:
        def f_native(ptr: ControllerPtr) -> None:
            geometry = Base().geometry(ptr)
            link = Base().link_get(ptr)
            cnt = Controller(geometry, self._runtime, self._handle, ptr, Recorder(self._handle, link))
            cnt = f(cnt)
            cnt._disposed = True

        f_native_ = ctypes.CFUNCTYPE(None, ControllerPtr)(f_native)
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future = Emu().emulator_record_from(self._ptr, int(t.total_seconds() * 1000 * 1000 * 1000), f_native_)  # type: ignore[arg-type]
        loop.call_soon(
            lambda *_: future.set_result(Emu().emulator_wait_result_record(self._handle, ffi_future)),
        )
        return Record(
            _validate_ptr(await future),
            self._handle,
        )

    def __del__(self: Self) -> None:
        self._dispose()

    def _dispose(self: Self) -> None:
        if self._ptr._0 is not None:
            Emu().emulator_free(self._ptr)
            self._ptr._0 = None

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self: Self,
        _exc_type: type[BaseException] | None,
        _exc_value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        self._dispose()


_Builder.into_emulator = lambda self: Emulator.__private_new__(self)  # type: ignore[method-assign]
