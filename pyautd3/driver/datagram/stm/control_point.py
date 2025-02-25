import ctypes
from typing import Self

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.native_methods.structs import Point3

# _pad is not required for python 3.12+?


class ControlPoint(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point", Point3),
        ("_offset", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]

    def __init__(self: Self, point: ArrayLike, phase_offset: Phase | None = None) -> None:
        super().__init__()
        self.point = np.array(point)
        self.phase_offset = phase_offset or Phase(0)

    @property
    def point(self: Self) -> np.ndarray:
        return self._point.ndarray()

    @point.setter
    def point(self: Self, value: ArrayLike) -> None:
        self._point = Point3(np.array(value))

    @property
    def phase_offset(self: Self) -> Phase:
        return Phase(self._offset)

    @phase_offset.setter
    def phase_offset(self: Self, value: Phase) -> None:
        self._offset = value.value


class ControlPoints1(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]


class ControlPoints2(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]


class ControlPoints3(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]


class ControlPoints4(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_point4", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]


class ControlPoints5(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_point4", ControlPoint),
        ("_point5", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]


class ControlPoints6(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_point4", ControlPoint),
        ("_point5", ControlPoint),
        ("_point6", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]


class ControlPoints7(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_point4", ControlPoint),
        ("_point5", ControlPoint),
        ("_point6", ControlPoint),
        ("_point7", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]


class ControlPoints8(ctypes.Structure):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_point4", ControlPoint),
        ("_point5", ControlPoint),
        ("_point6", ControlPoint),
        ("_point7", ControlPoint),
        ("_point8", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]


class ControlPoints:
    points: list[ControlPoint]
    intensity: EmitIntensity

    def __init__(self, points: list[ControlPoint] | list[ArrayLike], intensity: EmitIntensity | None = None) -> None:
        match points[0]:
            case ControlPoint():
                self.points = points  # type: ignore[assignment]
            case _:
                self.points = [ControlPoint(point=p) for p in points]
        self.intensity = intensity or EmitIntensity.MAX
