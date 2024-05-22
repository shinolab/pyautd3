import ctypes
from collections.abc import Callable

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga import Drive
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import ContextPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import Drive as _Drive
from pyautd3.native_methods.autd3capi_driver import GainPtr, GeometryPtr


class Custom(Gain["Custom"]):
    def __init__(self: "Custom", f: Callable[[Device], Callable[[Transducer], Drive]]) -> None:
        super().__init__()

        def f_native(_context: ContextPtr, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int, raw) -> None:  # noqa: ANN001
            dev = Device(dev_idx, Base().device(geometry_ptr, dev_idx))
            tr = Transducer(tr_idx, dev._ptr)
            d = f(dev)(tr)
            raw[0] = _Drive(d.phase.value, d.intensity.value)

        self._f_native = ctypes.CFUNCTYPE(None, ContextPtr, GeometryPtr, ctypes.c_uint32, ctypes.c_uint8, ctypes.POINTER(_Drive))(f_native)

    def _gain_ptr(self: "Custom", geometry: Geometry) -> GainPtr:
        return Base().gain_custom(self._f_native, ContextPtr(None), geometry._ptr)  # type: ignore[arg-type]
