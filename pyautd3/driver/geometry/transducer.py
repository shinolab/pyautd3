from ctypes import c_double

import numpy as np

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import (
    DevicePtr,
    TransducerPtr,
)


class Transducer:
    """Transducer."""

    _idx: int
    _ptr: TransducerPtr

    def __init__(self: "Transducer", idx: int, ptr: DevicePtr) -> None:
        self._idx = idx
        self._ptr = Base().transducer(ptr, idx)

    @property
    def idx(self: "Transducer") -> int:
        """Get the local index of the transducer."""
        return self._idx

    @property
    def position(self: "Transducer") -> np.ndarray:
        """Get the position of the transducer."""
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_position(self._ptr, vp)
        return v

    @property
    def rotation(self: "Transducer") -> np.ndarray:
        """Get the rotation of the transducer."""
        v = np.zeros([4]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_rotation(self._ptr, vp)
        return v

    @property
    def x_direction(self: "Transducer") -> np.ndarray:
        """Get the x-direction of the transducer."""
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_direction_x(self._ptr, vp)
        return v

    @property
    def y_direction(self: "Transducer") -> np.ndarray:
        """Get the y-direction of the transducer."""
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_direction_y(self._ptr, vp)
        return v

    @property
    def z_direction(self: "Transducer") -> np.ndarray:
        """Get the z-direction of the transducer."""
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_direction_z(self._ptr, vp)
        return v

    def wavelength(self: "Transducer", sound_speed: float) -> float:
        """Get the wavelength of the transducer.

        Arguments:
        ---------
            sound_speed: Sound speed [mm/s]
        """
        return float(Base().transducer_wavelength(self._ptr, sound_speed))

    def wavenumber(self: "Transducer", sound_speed: float) -> float:
        """Get the wavenumber of the transducer.

        Arguments:
        ---------
            sound_speed: Sound speed [mm/s]
        """
        return 2.0 * np.pi / self.wavelength(sound_speed)
