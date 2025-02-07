import ctypes
from abc import abstractmethod
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


class IControlPoints:
    @staticmethod
    @abstractmethod
    def _value() -> int:
        pass


class ControlPoints1(ctypes.Structure, IControlPoints):
    _fields_ = [  # noqa: RUF012
        ("_point", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]

    def __init__(self: Self, points: ArrayLike | ControlPoint, intensity: EmitIntensity | None = None) -> None:
        super().__init__()
        self.points = points  # type: ignore[assignment]
        self.intensity = intensity or EmitIntensity.maximum()

    @property
    def points(self: Self) -> np.ndarray:
        return np.array([self._point.point])

    @points.setter
    def points(self: Self, value: ArrayLike | ControlPoint) -> None:
        match value:
            case ControlPoint():
                self._point = value
            case _:
                self._point = ControlPoint(point=value)

    @property
    def intensity(self: Self) -> EmitIntensity:
        return EmitIntensity(self._intensity)

    @intensity.setter
    def intensity(self: Self, value: EmitIntensity) -> None:
        self._intensity = value.value

    @staticmethod
    def _value() -> int:
        return 1


class ControlPoints2(ctypes.Structure, IControlPoints):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]

    def __init__(
        self: Self,
        points: tuple[ArrayLike, ArrayLike] | tuple[ControlPoint, ControlPoint],
        intensity: EmitIntensity | None = None,
    ) -> None:
        super().__init__()
        self.points = points  # type: ignore[assignment]
        self.intensity = intensity or EmitIntensity.maximum()

    @property
    def points(self: Self) -> np.ndarray:
        return np.array([self._point1.point, self._point2.point])  # type: ignore[union-attr]

    @points.setter
    def points(
        self: Self,
        value: tuple[ArrayLike, ArrayLike] | tuple[ControlPoint, ControlPoint],
    ) -> None:
        match value:
            case (ControlPoint(), ControlPoint()):
                self._point1, self._point2 = value  # type: ignore[var-annotated]
            case _:
                self._point1, self._point2 = ControlPoint(point=value[0]), ControlPoint(point=value[1])

    @property
    def intensity(self: Self) -> EmitIntensity:
        return EmitIntensity(self._intensity)

    @intensity.setter
    def intensity(self: Self, value: EmitIntensity) -> None:
        self._intensity = value.value

    @staticmethod
    def _value() -> int:
        return 2


class ControlPoints3(ctypes.Structure, IControlPoints):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]

    def __init__(
        self: Self,
        points: tuple[ArrayLike, ArrayLike, ArrayLike] | tuple[ControlPoint, ControlPoint, ControlPoint],
        intensity: EmitIntensity | None = None,
    ) -> None:
        super().__init__()
        self.points = points  # type: ignore[assignment]
        self.intensity = intensity or EmitIntensity.maximum()

    @property
    def points(self: Self) -> np.ndarray:
        return np.array([self._point1.point, self._point2.point, self._point3.point])  # type: ignore[union-attr]

    @points.setter
    def points(
        self: Self,
        value: tuple[ArrayLike, ArrayLike, ArrayLike] | tuple[ControlPoint, ControlPoint, ControlPoint],
    ) -> None:
        match value:
            case (ControlPoint(), ControlPoint(), ControlPoint()):
                self._point1, self._point2, self._point3 = value  # type: ignore[var-annotated]
            case _:
                self._point1, self._point2, self._point3 = ControlPoint(point=value[0]), ControlPoint(point=value[1]), ControlPoint(point=value[2])

    @property
    def intensity(self: Self) -> EmitIntensity:
        return EmitIntensity(self._intensity)

    @intensity.setter
    def intensity(self: Self, value: EmitIntensity) -> None:
        self._intensity = value.value

    @staticmethod
    def _value() -> int:
        return 3


class ControlPoints4(ctypes.Structure, IControlPoints):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_point4", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]

    def __init__(
        self: Self,
        points: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike] | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint],
        intensity: EmitIntensity | None = None,
    ) -> None:
        super().__init__()
        self.points = points  # type: ignore[assignment]
        self.intensity = intensity or EmitIntensity.maximum()

    @property
    def points(self: Self) -> np.ndarray:
        return np.array([self._point1.point, self._point2.point, self._point3.point, self._point4.point])  # type: ignore[union-attr]

    @points.setter
    def points(
        self: Self,
        value: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike] | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint],
    ) -> None:
        match value:
            case (ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint()):
                self._point1, self._point2, self._point3, self._point4 = value  # type: ignore[var-annotated]
            case _:
                self._point1, self._point2, self._point3, self._point4 = (
                    ControlPoint(point=value[0]),
                    ControlPoint(point=value[1]),
                    ControlPoint(point=value[2]),
                    ControlPoint(point=value[3]),
                )

    @property
    def intensity(self: Self) -> EmitIntensity:
        return EmitIntensity(self._intensity)

    @intensity.setter
    def intensity(self: Self, value: EmitIntensity) -> None:
        self._intensity = value.value

    @staticmethod
    def _value() -> int:
        return 4


class ControlPoints5(ctypes.Structure, IControlPoints):
    _fields_ = [  # noqa: RUF012
        ("_point1", ControlPoint),
        ("_point2", ControlPoint),
        ("_point3", ControlPoint),
        ("_point4", ControlPoint),
        ("_point5", ControlPoint),
        ("_intensity", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8 * 3),
    ]

    def __init__(
        self: Self,
        points: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike]
        | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint],
        intensity: EmitIntensity | None = None,
    ) -> None:
        super().__init__()
        self.points = points  # type: ignore[assignment]
        self.intensity = intensity or EmitIntensity.maximum()

    @property
    def points(self: Self) -> np.ndarray:
        return np.array([self._point1.point, self._point2.point, self._point3.point, self._point4.point, self._point5.point])  # type: ignore[union-attr]

    @points.setter
    def points(
        self: Self,
        value: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike]
        | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint],
    ) -> None:
        match value:
            case (ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint()):
                self._point1, self._point2, self._point3, self._point4, self._point5 = value  # type: ignore[var-annotated]
            case _:
                self._point1, self._point2, self._point3, self._point4, self._point5 = (
                    ControlPoint(point=value[0]),
                    ControlPoint(point=value[1]),
                    ControlPoint(point=value[2]),
                    ControlPoint(point=value[3]),
                    ControlPoint(point=value[4]),
                )

    @property
    def intensity(self: Self) -> EmitIntensity:
        return EmitIntensity(self._intensity)

    @intensity.setter
    def intensity(self: Self, value: EmitIntensity) -> None:
        self._intensity = value.value

    @staticmethod
    def _value() -> int:
        return 5


class ControlPoints6(ctypes.Structure, IControlPoints):
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

    def __init__(
        self: Self,
        points: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike]
        | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint],
        intensity: EmitIntensity | None = None,
    ) -> None:
        super().__init__()
        self.points = points  # type: ignore[assignment]
        self.intensity = intensity or EmitIntensity.maximum()

    @property
    def points(self: Self) -> np.ndarray:
        return np.array(
            [
                self._point1.point,  # type: ignore[union-attr]
                self._point2.point,  # type: ignore[union-attr]
                self._point3.point,  # type: ignore[union-attr]
                self._point4.point,  # type: ignore[union-attr]
                self._point5.point,  # type: ignore[union-attr]
                self._point6.point,  # type: ignore[union-attr]
            ],
        )

    @points.setter
    def points(
        self: Self,
        value: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike]
        | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint],
    ) -> None:
        match value:
            case (ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint()):
                self._point1, self._point2, self._point3, self._point4, self._point5, self._point6 = value  # type: ignore[var-annotated]
            case _:
                self._point1, self._point2, self._point3, self._point4, self._point5, self._point6 = (
                    ControlPoint(point=value[0]),
                    ControlPoint(point=value[1]),
                    ControlPoint(point=value[2]),
                    ControlPoint(point=value[3]),
                    ControlPoint(point=value[4]),
                    ControlPoint(point=value[5]),
                )

    @property
    def intensity(self: Self) -> EmitIntensity:
        return EmitIntensity(self._intensity)

    @intensity.setter
    def intensity(self: Self, value: EmitIntensity) -> None:
        self._intensity = value.value

    @staticmethod
    def _value() -> int:
        return 6


class ControlPoints7(ctypes.Structure, IControlPoints):
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

    def __init__(
        self: Self,
        points: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike]
        | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint],
        intensity: EmitIntensity | None = None,
    ) -> None:
        super().__init__()
        self.points = points  # type: ignore[assignment]
        self.intensity = intensity or EmitIntensity.maximum()

    @property
    def points(self: Self) -> np.ndarray:
        return np.array(
            [
                self._point1.point,  # type: ignore[union-attr]
                self._point2.point,  # type: ignore[union-attr]
                self._point3.point,  # type: ignore[union-attr]
                self._point4.point,  # type: ignore[union-attr]
                self._point5.point,  # type: ignore[union-attr]
                self._point6.point,  # type: ignore[union-attr]
                self._point7.point,  # type: ignore[union-attr]
            ],
        )

    @points.setter
    def points(
        self: Self,
        value: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike]
        | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint],
    ) -> None:
        match value:
            case (ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint()):
                (
                    self._point1,
                    self._point2,
                    self._point3,
                    self._point4,
                    self._point5,
                    self._point6,
                    self._point7,
                ) = value  # type: ignore[var-annotated]
            case _:
                self._point1, self._point2, self._point3, self._point4, self._point5, self._point6, self._point7 = (
                    ControlPoint(point=value[0]),
                    ControlPoint(point=value[1]),
                    ControlPoint(point=value[2]),
                    ControlPoint(point=value[3]),
                    ControlPoint(point=value[4]),
                    ControlPoint(point=value[5]),
                    ControlPoint(point=value[6]),
                )

    @property
    def intensity(self: Self) -> EmitIntensity:
        return EmitIntensity(self._intensity)

    @intensity.setter
    def intensity(self: Self, value: EmitIntensity) -> None:
        self._intensity = value.value

    @staticmethod
    def _value() -> int:
        return 7


class ControlPoints8(ctypes.Structure, IControlPoints):
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

    def __init__(
        self: Self,
        points: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike]
        | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint],
        intensity: EmitIntensity | None = None,
    ) -> None:
        super().__init__()
        self.points = points  # type: ignore[assignment]
        self.intensity = intensity or EmitIntensity.maximum()

    @property
    def points(self: Self) -> np.ndarray:
        return np.array(
            [
                self._point1.point,  # type: ignore[union-attr]
                self._point2.point,  # type: ignore[union-attr]
                self._point3.point,  # type: ignore[union-attr]
                self._point4.point,  # type: ignore[union-attr]
                self._point5.point,  # type: ignore[union-attr]
                self._point6.point,  # type: ignore[union-attr]
                self._point7.point,  # type: ignore[union-attr]
                self._point8.point,  # type: ignore[union-attr]
            ],
        )

    @points.setter
    def points(
        self: Self,
        value: tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike]
        | tuple[ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint, ControlPoint],
    ) -> None:
        match value:
            case (ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint(), ControlPoint()):
                (
                    self._point1,
                    self._point2,
                    self._point3,
                    self._point4,
                    self._point5,
                    self._point6,
                    self._point7,
                    self._point8,
                ) = value  # type: ignore[var-annotated]
            case _:
                self._point1, self._point2, self._point3, self._point4, self._point5, self._point6, self._point7, self._point8 = (
                    ControlPoint(point=value[0]),
                    ControlPoint(point=value[1]),
                    ControlPoint(point=value[2]),
                    ControlPoint(point=value[3]),
                    ControlPoint(point=value[4]),
                    ControlPoint(point=value[5]),
                    ControlPoint(point=value[6]),
                    ControlPoint(point=value[7]),
                )

    @property
    def intensity(self: Self) -> EmitIntensity:
        return EmitIntensity(self._intensity)

    @intensity.setter
    def intensity(self: Self, value: EmitIntensity) -> None:
        self._intensity = value.value

    @staticmethod
    def _value() -> int:
        return 8
