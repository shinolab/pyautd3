import functools
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from ctypes import POINTER
from typing import Generic, TypeVar

import numpy as np

from pyautd3.driver.datagram.gain.gain import Gain as _Gain
from pyautd3.driver.firmware.fpga import Drive
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import Drive as _Drive
from pyautd3.native_methods.autd3capi_driver import GainPtr

G = TypeVar("G", bound="Gain")


class Gain(_Gain[G], Generic[G], metaclass=ABCMeta):
    @abstractmethod
    def calc(self: "Gain[G]", geometry: Geometry) -> dict[int, np.ndarray]:
        pass

    def _gain_ptr(self: "Gain[G]", geometry: Geometry) -> GainPtr:
        drives = self.calc(geometry)
        return functools.reduce(
            lambda acc, dev: Base().gain_raw_set(
                acc,
                dev.idx,
                drives[dev.idx].ctypes.data_as(POINTER(_Drive)),  # type: ignore[arg-type]
                len(drives[dev.idx]),
            ),
            geometry.devices,
            Base().gain_raw(),
        )

    @staticmethod
    def _transform(geometry: Geometry, f: Callable[[Device], Callable[[Transducer], Drive]]) -> dict[int, np.ndarray]:
        return {
            dev.idx: np.fromiter(
                (np.void(_Drive(d.phase._value, d.intensity._value)) for d in (f(dev)(tr) for tr in dev)),  # type: ignore[call-overload]
                dtype=_Drive,
            )
            for dev in geometry.devices
        }
