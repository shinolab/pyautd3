import asyncio
import ctypes
from collections.abc import Callable
from types import TracebackType
from typing import Self

import numpy as np
import polars as pl

from pyautd3.controller.controller import Controller, _Builder
from pyautd3.driver.geometry.geometry import Geometry
from pyautd3.driver.link import Link
from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.native_methods.autd3_driver import DcSysTime as _DcSysTime
from pyautd3.native_methods.autd3capi import ControllerPtr, RuntimePtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GeometryPtr, HandlePtr, LinkPtr
from pyautd3.native_methods.autd3capi_emulator import EmulatorPtr, InstantPtr, RecordPtr, RmsPtr
from pyautd3.native_methods.autd3capi_emulator import InstantRecordOption as InstantRecordOption_
from pyautd3.native_methods.autd3capi_emulator import NativeMethods as Emu
from pyautd3.native_methods.autd3capi_emulator import Range as Range_
from pyautd3.native_methods.autd3capi_emulator import RmsRecordOption as RmsRecordOption_
from pyautd3.native_methods.utils import _validate_ptr, _validate_status
from pyautd3.utils import Duration


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


class InstantRecordOption:
    _inner: InstantRecordOption_

    def __init__(
        self: Self,
        *,
        sound_speed: float | None = None,
        time_step: Duration | None = None,
        print_progress: bool | None = None,
        memory_limits_hint_mb: int | None = None,
        gpu: bool | None = None,
    ) -> None:
        self._inner = InstantRecordOption_(
            sound_speed or 340e3,
            (time_step or Duration.from_micros(1))._inner,
            print_progress or False,
            memory_limits_hint_mb or 128,
            gpu or False,
        )


class RmsRecordOption:
    _inner: RmsRecordOption_

    def __init__(
        self: Self,
        *,
        sound_speed: float | None = None,
        print_progress: bool | None = None,
        gpu: bool | None = None,
    ) -> None:
        self._inner = RmsRecordOption_(
            sound_speed or 340e3,
            print_progress or False,
            gpu or False,
        )


class Instant:
    _ptr: InstantPtr
    _handle: HandlePtr

    def __init__(self: Self, ptr: InstantPtr, handle: HandlePtr) -> None:
        self._ptr = ptr
        self._handle = handle

    def __del__(self: Self) -> None:
        self._dispose()

    def _dispose(self: Self) -> None:
        if self._ptr._0 is not None:  # pragma: no cover
            Emu().emulator_sound_field_instant_free(self._ptr)
            self._ptr._0 = None

    def skip(self: Self, duration: Duration) -> Self:
        _validate_status(
            Base().wait_local_result_status(
                self._handle,
                Emu().emulator_sound_field_instant_skip(self._ptr, duration._inner),
            ),
        )
        return self

    def next(self: Self, duration: Duration) -> pl.DataFrame:
        n = int(Emu().emulator_sound_field_instant_time_len(self._ptr, duration._inner))
        points_len = int(Emu().emulator_sound_field_instant_points_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)

        x = np.zeros(points_len, dtype=np.float32)
        y = np.zeros(points_len, dtype=np.float32)
        z = np.zeros(points_len, dtype=np.float32)
        Emu().emulator_sound_field_instant_get_x(self._ptr, x.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_instant_get_y(self._ptr, y.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_instant_get_z(self._ptr, z.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]

        v = np.zeros([n, points_len], dtype=np.float32)
        _validate_status(
            Base().wait_local_result_status(
                self._handle,
                Emu().emulator_sound_field_instant_next(
                    self._ptr,
                    duration._inner,
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

    async def next_async(self: Self, duration: Duration) -> pl.DataFrame:
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()

        n = int(Emu().emulator_sound_field_instant_time_len(self._ptr, duration._inner))
        points_len = int(Emu().emulator_sound_field_instant_points_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)

        x = np.zeros(points_len, dtype=np.float32)
        y = np.zeros(points_len, dtype=np.float32)
        z = np.zeros(points_len, dtype=np.float32)
        Emu().emulator_sound_field_instant_get_x(self._ptr, x.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_instant_get_y(self._ptr, y.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_instant_get_z(self._ptr, z.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]

        v = np.zeros([n, points_len], dtype=np.float32)
        ffi_future = Emu().emulator_sound_field_instant_next(
            self._ptr,
            duration._inner,
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


class Rms:
    _ptr: RmsPtr
    _handle: HandlePtr

    def __init__(self: Self, ptr: RmsPtr, handle: HandlePtr) -> None:
        self._ptr = ptr
        self._handle = handle

    def __del__(self: Self) -> None:
        self._dispose()

    def _dispose(self: Self) -> None:
        if self._ptr._0 is not None:  # pragma: no cover
            Emu().emulator_sound_field_rms_free(self._ptr)
            self._ptr._0 = None

    def skip(self: Self, duration: Duration) -> Self:
        _validate_status(
            Base().wait_local_result_status(
                self._handle,
                Emu().emulator_sound_field_rms_skip(self._ptr, duration._inner),
            ),
        )
        return self

    def next(self: Self, duration: Duration) -> pl.DataFrame:
        n = int(Emu().emulator_sound_field_rms_time_len(self._ptr, duration._inner))
        points_len = int(Emu().emulator_sound_field_rms_points_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)

        x = np.zeros(points_len, dtype=np.float32)
        y = np.zeros(points_len, dtype=np.float32)
        z = np.zeros(points_len, dtype=np.float32)
        Emu().emulator_sound_field_rms_get_x(self._ptr, x.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_rms_get_y(self._ptr, y.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_rms_get_z(self._ptr, z.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]

        v = np.zeros([n, points_len], dtype=np.float32)
        _validate_status(
            Base().wait_local_result_status(
                self._handle,
                Emu().emulator_sound_field_rms_next(
                    self._ptr,
                    duration._inner,
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

    async def next_async(self: Self, duration: Duration) -> pl.DataFrame:
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()

        n = int(Emu().emulator_sound_field_rms_time_len(self._ptr, duration._inner))
        points_len = int(Emu().emulator_sound_field_rms_points_len(self._ptr))
        time = np.zeros(n, dtype=np.uint64)

        x = np.zeros(points_len, dtype=np.float32)
        y = np.zeros(points_len, dtype=np.float32)
        z = np.zeros(points_len, dtype=np.float32)
        Emu().emulator_sound_field_rms_get_x(self._ptr, x.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_rms_get_y(self._ptr, y.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]
        Emu().emulator_sound_field_rms_get_z(self._ptr, z.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))  # type: ignore[arg-type]

        v = np.zeros([n, points_len], dtype=np.float32)
        ffi_future = Emu().emulator_sound_field_rms_next(
            self._ptr,
            duration._inner,
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

    def tick(self: Self, tick: Duration) -> None:
        _validate_status(
            Emu().emulator_tick_ns(self._ptr, tick._inner),
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

    def sound_field(self: Self, range_: Range, option: InstantRecordOption | RmsRecordOption) -> Instant | Rms:
        match option:
            case InstantRecordOption():
                return Instant(
                    _validate_ptr(
                        Emu().emulator_sound_field_instant_wait(
                            self._handle,
                            Emu().emulator_sound_field_instant(self._ptr, range_._inner, option._inner),
                        ),
                    ),
                    self._handle,
                )
            case RmsRecordOption():  # pragma: no cover
                return Rms(
                    _validate_ptr(
                        Emu().emulator_sound_field_rms_wait(
                            self._handle,
                            Emu().emulator_sound_field_rms(self._ptr, range_._inner, option._inner),
                        ),
                    ),
                    self._handle,
                )

    async def sound_field_async(self: Self, range_: Range, option: InstantRecordOption | RmsRecordOption) -> Instant | Rms:
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        match option:
            case InstantRecordOption():
                ffi_future = Emu().emulator_sound_field_instant(self._ptr, range_._inner, option._inner)
                loop.call_soon(
                    lambda *_: future.set_result(Emu().emulator_sound_field_instant_wait(self._handle, ffi_future)),
                )
                return Instant(
                    _validate_ptr(await future),
                    self._handle,
                )
            case RmsRecordOption():  # pragma: no cover
                ffi_future = Emu().emulator_sound_field_rms(self._ptr, range_._inner, option._inner)
                loop.call_soon(
                    lambda *_: future.set_result(Emu().emulator_sound_field_rms_wait(self._handle, ffi_future)),
                )
                return Rms(
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
        return self.record_from(DcSysTime.__private_new__(_DcSysTime(0)), f)

    async def record_async(self: Self, f: Callable[[Controller[Recorder]], Controller[Recorder]]) -> Record:
        return await self.record_from_async(DcSysTime.__private_new__(_DcSysTime(0)), f)

    def record_from(self: Self, start_time: DcSysTime, f: Callable[[Controller[Recorder]], Controller[Recorder]]) -> Record:
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
                    Emu().emulator_record_from(self._ptr, start_time._inner, f_native_),  # type: ignore[arg-type]
                ),
            ),
            self._handle,
        )

    async def record_from_async(self: Self, start_time: DcSysTime, f: Callable[[Controller[Recorder]], Controller[Recorder]]) -> Record:
        def f_native(ptr: ControllerPtr) -> None:
            geometry = Base().geometry(ptr)
            link = Base().link_get(ptr)
            cnt = Controller(geometry, self._runtime, self._handle, ptr, Recorder(self._handle, link))
            cnt = f(cnt)
            cnt._disposed = True

        f_native_ = ctypes.CFUNCTYPE(None, ControllerPtr)(f_native)
        future: asyncio.Future = asyncio.Future()
        loop = asyncio.get_event_loop()
        ffi_future = Emu().emulator_record_from(self._ptr, start_time._inner, f_native_)  # type: ignore[arg-type]
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
