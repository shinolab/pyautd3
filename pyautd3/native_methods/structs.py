import ctypes
from typing import Self
import numpy as np


class FfiFuture(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_byte * 24)]


class LocalFfiFuture(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_byte * 24)]


class Vector3(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float), ("z", ctypes.c_float)]

    def __init__(self: Self, v: np.ndarray) -> None:
        self.x = v[0]
        self.y = v[1]
        self.z = v[2]

    def ndarray(self):
        return np.array([self.x, self.y, self.z])


class Quaternion(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float), ("z", ctypes.c_float), ("w", ctypes.c_float)]

    def __init__(self: Self, v: np.ndarray) -> None:
        self.w = v[0]
        self.x = v[1]
        self.y = v[2]
        self.z = v[3]

    def ndarray(self):
        return np.array([self.w, self.x, self.y, self.z])
