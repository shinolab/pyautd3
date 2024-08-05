import ctypes
from collections.abc import Callable
from typing import Generic, TypeVar

from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment import IntoDatagramWithSegment
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.firmware.fpga import Drive, Phase
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import Drive as _Drive
from pyautd3.native_methods.autd3capi_driver import GainPtr, GeometryPtr

from .cache import IntoGainCache

G = TypeVar("G", bound=GainBase)


class Transform(
    IntoGainCache["Transform[G]"],
    IntoDatagramWithSegment["Transform[G]"],
    IntoDatagramWithTimeout["Transform[G]"],
    IntoDatagramWithParallelThreshold["Transform[G]"],
    GainBase,
    Generic[G],
):
    _g: G

    def __init__(self: "Transform", g: G, f: Callable[[Device], Callable[[Transducer, Drive], Drive | EmitIntensity | Phase | tuple]]) -> None:
        super().__init__()
        self._g = g

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int, src, raw) -> None:  # noqa: ANN001
            dev = Device(dev_idx, geometry_ptr)
            tr = Transducer(tr_idx, dev._ptr)
            d = Drive(f(dev)(tr, Drive((Phase(src.phase), EmitIntensity(src.intensity)))))
            raw[0] = _Drive(d.phase.value, d.intensity.value)

        self._f_native = ctypes.CFUNCTYPE(None, ctypes.c_void_p, GeometryPtr, ctypes.c_uint16, ctypes.c_uint8, _Drive, ctypes.POINTER(_Drive))(
            f_native,
        )

    def _gain_ptr(self: "Transform[G]", geometry: Geometry) -> GainPtr:
        return Base().gain_with_transform(
            self._g._gain_ptr(geometry),
            self._f_native,  # type: ignore[arg-type]
            None,
            geometry._ptr,
        )


class IntoGainTransform(GainBase, Generic[G]):
    def with_transform(self: G, f: Callable[[Device], Callable[[Transducer, Drive], Drive | EmitIntensity | Phase | tuple]]) -> Transform[G]:
        return Transform(self, f)
