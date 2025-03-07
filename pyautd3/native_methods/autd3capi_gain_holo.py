import ctypes
import enum
import threading
from pathlib import Path

from pyautd3.native_methods.autd3 import EmitIntensity
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Point3


class EmissionConstraintTag(enum.IntEnum):
    Normalize = 1
    Uniform = 2
    Multiply = 3
    Clamp = 4

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class EmissionConstraintValue(ctypes.Union):
    _fields_ = [("null", EmitIntensity), ("uniform", EmitIntensity), ("multiply", ctypes.c_float), ("clamp", EmitIntensity * 2)]


class EmissionConstraintWrap(ctypes.Structure):
    _fields_ = [("tag", ctypes.c_uint8), ("value", EmissionConstraintValue)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmissionConstraintWrap) and self._fields_ == other._fields_  # pragma: no cover


class BackendPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BackendPtr) and self._fields_ == other._fields_  # pragma: no cover


class NaiveOption(ctypes.Structure):
    _fields_ = [("constraint", EmissionConstraintWrap)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NaiveOption) and self._fields_ == other._fields_  # pragma: no cover


class GSPATOption(ctypes.Structure):
    _fields_ = [("constraint", EmissionConstraintWrap), ("repeat", ctypes.c_uint32)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GSPATOption) and self._fields_ == other._fields_  # pragma: no cover


class LMOption(ctypes.Structure):
    _fields_ = [
        ("constraint", EmissionConstraintWrap),
        ("eps_1", ctypes.c_float),
        ("eps_2", ctypes.c_float),
        ("tau", ctypes.c_float),
        ("k_max", ctypes.c_uint32),
        ("initial", ctypes.POINTER(ctypes.c_float)),
        ("initial_len", ctypes.c_uint32),
    ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LMOption) and self._fields_ == other._fields_  # pragma: no cover


class GreedyOption(ctypes.Structure):
    _fields_ = [("constraint", EmissionConstraintWrap), ("phase_div", ctypes.c_uint8)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GreedyOption) and self._fields_ == other._fields_  # pragma: no cover


class GSOption(ctypes.Structure):
    _fields_ = [("constraint", EmissionConstraintWrap), ("repeat", ctypes.c_uint32)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GSOption) and self._fields_ == other._fields_  # pragma: no cover


class Singleton(type):
    _instances = {}  # type: ignore[var-annotated]
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:  # pragma: no cover
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):
    def init_dll(self, bin_location: Path, bin_prefix: str, bin_ext: str) -> None:
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi_gain_holo{bin_ext}"))

        self.dll.AUTDGainHoloConstraintNormalize.argtypes = []
        self.dll.AUTDGainHoloConstraintNormalize.restype = EmissionConstraintWrap

        self.dll.AUTDGainHoloConstraintUniform.argtypes = [EmitIntensity]
        self.dll.AUTDGainHoloConstraintUniform.restype = EmissionConstraintWrap

        self.dll.AUTDGainHoloConstraintMultiply.argtypes = [ctypes.c_float]
        self.dll.AUTDGainHoloConstraintMultiply.restype = EmissionConstraintWrap

        self.dll.AUTDGainHoloConstraintClamp.argtypes = [EmitIntensity, EmitIntensity]
        self.dll.AUTDGainHoloConstraintClamp.restype = EmissionConstraintWrap

        self.dll.AUTDGainHoloGreedySphere.argtypes = [ctypes.POINTER(Point3), ctypes.POINTER(ctypes.c_float), ctypes.c_uint32, GreedyOption]
        self.dll.AUTDGainHoloGreedySphere.restype = GainPtr

        self.dll.AUTDGainGreedyIsDefault.argtypes = [GreedyOption]
        self.dll.AUTDGainGreedyIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainHoloGSSphere.argtypes = [BackendPtr, ctypes.POINTER(Point3), ctypes.POINTER(ctypes.c_float), ctypes.c_uint32, GSOption]
        self.dll.AUTDGainHoloGSSphere.restype = GainPtr

        self.dll.AUTDGainGSIsDefault.argtypes = [GSOption]
        self.dll.AUTDGainGSIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainHoloGSPATSphere.argtypes = [BackendPtr, ctypes.POINTER(Point3), ctypes.POINTER(ctypes.c_float), ctypes.c_uint32, GSPATOption]
        self.dll.AUTDGainHoloGSPATSphere.restype = GainPtr

        self.dll.AUTDGainGSPATIsDefault.argtypes = [GSPATOption]
        self.dll.AUTDGainGSPATIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainHoloSPLToPascal.argtypes = [ctypes.c_float]
        self.dll.AUTDGainHoloSPLToPascal.restype = ctypes.c_float

        self.dll.AUTDGainHoloPascalToSPL.argtypes = [ctypes.c_float]
        self.dll.AUTDGainHoloPascalToSPL.restype = ctypes.c_float

        self.dll.AUTDGainHoloLMSphere.argtypes = [BackendPtr, ctypes.POINTER(Point3), ctypes.POINTER(ctypes.c_float), ctypes.c_uint32, LMOption]
        self.dll.AUTDGainHoloLMSphere.restype = GainPtr

        self.dll.AUTDGainLMIsDefault.argtypes = [LMOption]
        self.dll.AUTDGainLMIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainHoloNaiveSphere.argtypes = [BackendPtr, ctypes.POINTER(Point3), ctypes.POINTER(ctypes.c_float), ctypes.c_uint32, NaiveOption]
        self.dll.AUTDGainHoloNaiveSphere.restype = GainPtr

        self.dll.AUTDGainNaiveIsDefault.argtypes = [NaiveOption]
        self.dll.AUTDGainNaiveIsDefault.restype = ctypes.c_bool

        self.dll.AUTDNalgebraBackendSphere.argtypes = []
        self.dll.AUTDNalgebraBackendSphere.restype = BackendPtr

        self.dll.AUTDDeleteNalgebraBackendSphere.argtypes = [BackendPtr]
        self.dll.AUTDDeleteNalgebraBackendSphere.restype = None

    def gain_holo_constraint_normalize(self) -> EmissionConstraintWrap:
        return self.dll.AUTDGainHoloConstraintNormalize()

    def gain_holo_constraint_uniform(self, intensity: EmitIntensity) -> EmissionConstraintWrap:
        return self.dll.AUTDGainHoloConstraintUniform(intensity)

    def gain_holo_constraint_multiply(self, v: float) -> EmissionConstraintWrap:
        return self.dll.AUTDGainHoloConstraintMultiply(v)

    def gain_holo_constraint_clamp(self, min_v: EmitIntensity, max_v: EmitIntensity) -> EmissionConstraintWrap:
        return self.dll.AUTDGainHoloConstraintClamp(min_v, max_v)

    def gain_holo_greedy_sphere(self, points: ctypes.Array[Point3], amps: ctypes.Array[ctypes.c_float], size: int, option: GreedyOption) -> GainPtr:
        return self.dll.AUTDGainHoloGreedySphere(points, amps, size, option)

    def gain_greedy_is_default(self, option: GreedyOption) -> ctypes.c_bool:
        return self.dll.AUTDGainGreedyIsDefault(option)

    def gain_holo_gs_sphere(
        self,
        backend: BackendPtr,
        points: ctypes.Array[Point3],
        amps: ctypes.Array[ctypes.c_float],
        size: int,
        option: GSOption,
    ) -> GainPtr:
        return self.dll.AUTDGainHoloGSSphere(backend, points, amps, size, option)

    def gain_gs_is_default(self, option: GSOption) -> ctypes.c_bool:
        return self.dll.AUTDGainGSIsDefault(option)

    def gain_holo_gspat_sphere(
        self,
        backend: BackendPtr,
        points: ctypes.Array[Point3],
        amps: ctypes.Array[ctypes.c_float],
        size: int,
        option: GSPATOption,
    ) -> GainPtr:
        return self.dll.AUTDGainHoloGSPATSphere(backend, points, amps, size, option)

    def gain_gspat_is_default(self, option: GSPATOption) -> ctypes.c_bool:
        return self.dll.AUTDGainGSPATIsDefault(option)

    def gain_holo_spl_to_pascal(self, value: float) -> ctypes.c_float:
        return self.dll.AUTDGainHoloSPLToPascal(value)

    def gain_holo_pascal_to_spl(self, value: float) -> ctypes.c_float:
        return self.dll.AUTDGainHoloPascalToSPL(value)

    def gain_holo_lm_sphere(
        self,
        backend: BackendPtr,
        points: ctypes.Array[Point3],
        amps: ctypes.Array[ctypes.c_float],
        size: int,
        option: LMOption,
    ) -> GainPtr:
        return self.dll.AUTDGainHoloLMSphere(backend, points, amps, size, option)

    def gain_lm_is_default(self, option: LMOption) -> ctypes.c_bool:
        return self.dll.AUTDGainLMIsDefault(option)

    def gain_holo_naive_sphere(
        self,
        backend: BackendPtr,
        points: ctypes.Array[Point3],
        amps: ctypes.Array[ctypes.c_float],
        size: int,
        option: NaiveOption,
    ) -> GainPtr:
        return self.dll.AUTDGainHoloNaiveSphere(backend, points, amps, size, option)

    def gain_naive_is_default(self, option: NaiveOption) -> ctypes.c_bool:
        return self.dll.AUTDGainNaiveIsDefault(option)

    def nalgebra_backend_sphere(self) -> BackendPtr:
        return self.dll.AUTDNalgebraBackendSphere()

    def delete_nalgebra_backend_sphere(self, backend: BackendPtr) -> None:
        return self.dll.AUTDDeleteNalgebraBackendSphere(backend)
