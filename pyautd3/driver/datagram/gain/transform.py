from collections.abc import Callable
from ctypes import POINTER
from functools import reduce
from typing import Generic, TypeVar

import numpy as np

from pyautd3.driver.common.drive import Drive
from pyautd3.driver.common.phase import Phase
from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.with_segment import IntoDatagramWithSegment
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import Drive as _Drive
from pyautd3.native_methods.autd3capi_def import GainPtr
from pyautd3.native_methods.utils import _validate_ptr

from .cache import IntoGainCache

G = TypeVar("G", bound=GainBase)


class Transform(
    IntoDatagramWithSegment["Transform[G]"],
    IntoGainCache["Transform[G]"],
    GainBase,
    Generic[G],
):
    """Gain to transform gain data."""

    _g: G
    _f: Callable[[Device, Transducer, Drive], Drive]

    def __init__(self: "Transform", g: G, f: Callable[[Device, Transducer, Drive], Drive]) -> None:
        super().__init__()
        self._g = g
        self._f = f

    def _gain_ptr(self: "Transform[G]", geometry: Geometry) -> GainPtr:
        res = _validate_ptr(Base().gain_calc(self._g._gain_ptr(geometry), geometry._geometry_ptr()))

        drives: dict[int, np.ndarray] = {}
        for dev in geometry.devices:
            d = np.zeros(dev.num_transducers, dtype=_Drive)

            Base().gain_calc_get_result(res, d.ctypes.data_as(POINTER(_Drive)), dev.idx)  # type: ignore[arg-type]
            for tr in dev:
                drive = self._f(dev, tr, Drive(Phase(int(d[tr.idx]["phase"])), int(d[tr.idx]["intensity"])))
                d[tr.idx] = np.void(_Drive(drive.phase._value, drive.intensity._value))  # type: ignore[call-overload]
            drives[dev.idx] = d

        Base().gain_calc_free_result(res)

        return reduce(
            lambda acc, dev: Base().gain_custom_set(
                acc,
                dev.idx,
                drives[dev.idx].ctypes.data_as(POINTER(_Drive)),  # type: ignore[arg-type]
                len(drives[dev.idx]),
            ),
            geometry.devices,
            Base().gain_custom(),
        )


class IntoGainTransform(GainBase, Generic[G]):
    """Gain interface of Transform."""

    def with_transform(self: G, f: Callable[[Device, Transducer, Drive], Drive]) -> Transform[G]:
        """Transform the result of calculation.

        Arguments:
        ---------
            self: Gain
            f: Transform function. The first argument is device, the second is transducer, and the third is the original drive data.

        """
        return Transform(self, f)
