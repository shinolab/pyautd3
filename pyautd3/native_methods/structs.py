import ctypes
from typing import Self

import numpy as np


class Vector3(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float), ("z", ctypes.c_float)]

    def __init__(self: Self, v: np.ndarray) -> None:
        self.x = v[0]
        self.y = v[1]
        self.z = v[2]

    def ndarray(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])


class Point3(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float), ("z", ctypes.c_float)]

    def __init__(self: Self, v: np.ndarray) -> None:
        self.x = v[0]
        self.y = v[1]
        self.z = v[2]

    def ndarray(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])


class Quaternion(ctypes.Structure):
    _fields_ = [("w", ctypes.c_float), ("i", ctypes.c_float), ("j", ctypes.c_float), ("k", ctypes.c_float)]

    def __init__(self: Self, v: np.ndarray) -> None:
        self.w = v[0]
        self.i = v[1]
        self.j = v[2]
        self.k = v[3]

    def ndarray(self) -> np.ndarray:
        return np.array([self.w, self.i, self.j, self.k])


class PulseWidth(ctypes.Structure):
    _fields_ = [("value", ctypes.c_uint64)]
