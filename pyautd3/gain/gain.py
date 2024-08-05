import ctypes
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import Generic, TypeVar

from pyautd3.driver.datagram.gain.gain import Gain as _Gain
from pyautd3.driver.firmware.fpga import Drive
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ConstPtr, GainPtr, GeometryPtr
from pyautd3.native_methods.autd3capi_driver import Drive as _Drive

G = TypeVar("G", bound="Gain")


class Gain(_Gain[G], Generic[G], metaclass=ABCMeta):
    @abstractmethod
    def calc(self: "Gain[G]", geometry: Geometry) -> Callable[[Device], Callable[[Transducer], Drive | EmitIntensity | Phase | tuple]]:
        pass

    def _gain_ptr(self: "Gain[G]", geometry: Geometry) -> GainPtr:
        f = self.calc(geometry)

        def f_native(_context: ConstPtr, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int, raw) -> None:  # noqa: ANN001
            dev = Device(dev_idx, geometry_ptr)
            tr = Transducer(tr_idx, dev._ptr)
            d = Drive(f(dev)(tr))
            raw[0] = _Drive(d.phase.value, d.intensity.value)

        self._f_native = ctypes.CFUNCTYPE(None, ConstPtr, GeometryPtr, ctypes.c_uint16, ctypes.c_uint8, ctypes.POINTER(_Drive))(f_native)

        return Base().gain_custom(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]

    @staticmethod
    def _transform(
        f: Callable[[Device], Callable[[Transducer], Drive | EmitIntensity | Phase | tuple]],
    ) -> Callable[[Device], Callable[[Transducer], Drive | EmitIntensity | Phase | tuple]]:
        return f
