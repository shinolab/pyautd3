import ctypes
from collections.abc import Callable
from typing import Self

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga import Drive
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3 import Drive as Drive_
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ConstPtr, GainPtr, GeometryPtr


class Custom(Gain):
    def __init__(self: Self, f: Callable[[Device], Callable[[Transducer], Drive]]) -> None:
        super().__init__()

        dev_cache: dict[int, Device] = {}
        fn_cache: dict[int, Callable[[Transducer], Drive]] = {}

        def f_native(_context: ConstPtr, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int, raw) -> None:  # noqa: ANN001

            dev = dev_cache.get(dev_idx)
            if dev is None:
                dev = Device(dev_idx, geometry_ptr)
                dev_cache[dev_idx] = dev

            fn = fn_cache.get(dev_idx)
            if fn is None:
                fn = f(dev)
                fn_cache[dev_idx] = fn

            tr = Transducer(tr_idx, dev_idx, dev._ptr)

            d = fn(tr)
            raw[0] = Drive_(d.phase._inner(), d.intensity._inner())

        self._f_native = ctypes.CFUNCTYPE(None, ConstPtr, GeometryPtr, ctypes.c_uint16, ctypes.c_uint8, ctypes.POINTER(Drive_))(f_native)

    def _gain_ptr(self: Self, geometry: Geometry) -> GainPtr:
        return Base().gain_custom(self._f_native, ctypes.c_void_p(None), geometry._geometry_ptr)  # type: ignore[bad-argument-type]
