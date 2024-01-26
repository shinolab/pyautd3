# This file is autogenerated
import threading
import ctypes
import os
from pyautd3.native_methods.autd3capi_def import GainPtr


class EmissionConstraintPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class BackendPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class ResultBackend(ctypes.Structure):
    _fields_ = [("result", BackendPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


class Singleton(type):
    _instances = {}  # type: ignore
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):

    def init_dll(self, bin_location: str, bin_prefix: str, bin_ext: str):
        try:
            self.dll = ctypes.CDLL(os.path.join(bin_location, f'{bin_prefix}autd3capi_gain_holo{bin_ext}'))
        except Exception:
            return

        self.dll.AUTDGainHoloConstraintDotCare.argtypes = [] 
        self.dll.AUTDGainHoloConstraintDotCare.restype = EmissionConstraintPtr

        self.dll.AUTDGainHoloConstraintNormalize.argtypes = [] 
        self.dll.AUTDGainHoloConstraintNormalize.restype = EmissionConstraintPtr

        self.dll.AUTDGainHoloConstraintUniform.argtypes = [ctypes.c_uint8] 
        self.dll.AUTDGainHoloConstraintUniform.restype = EmissionConstraintPtr

        self.dll.AUTDGainHoloConstraintClamp.argtypes = [ctypes.c_uint8, ctypes.c_uint8] 
        self.dll.AUTDGainHoloConstraintClamp.restype = EmissionConstraintPtr

        self.dll.AUTDGainHoloGreedy.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_uint64, ctypes.c_uint8, EmissionConstraintPtr]  # type: ignore 
        self.dll.AUTDGainHoloGreedy.restype = GainPtr

        self.dll.AUTDGainGreedyIsDefault.argtypes = [GainPtr]  # type: ignore 
        self.dll.AUTDGainGreedyIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainHoloGS.argtypes = [BackendPtr, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_uint64, ctypes.c_uint32, EmissionConstraintPtr]  # type: ignore 
        self.dll.AUTDGainHoloGS.restype = GainPtr

        self.dll.AUTDGainGSIsDefault.argtypes = [GainPtr]  # type: ignore 
        self.dll.AUTDGainGSIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainHoloGSPAT.argtypes = [BackendPtr, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_uint64, ctypes.c_uint32, EmissionConstraintPtr]  # type: ignore 
        self.dll.AUTDGainHoloGSPAT.restype = GainPtr

        self.dll.AUTDGainGSPATIsDefault.argtypes = [GainPtr]  # type: ignore 
        self.dll.AUTDGainGSPATIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainHoloSPLToPascal.argtypes = [ctypes.c_double] 
        self.dll.AUTDGainHoloSPLToPascal.restype = ctypes.c_double

        self.dll.AUTDGainHoloPascalToSPL.argtypes = [ctypes.c_double] 
        self.dll.AUTDGainHoloPascalToSPL.restype = ctypes.c_double

        self.dll.AUTDGainHoloLM.argtypes = [BackendPtr, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_uint64, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_uint32, ctypes.POINTER(ctypes.c_double), ctypes.c_uint64, EmissionConstraintPtr]  # type: ignore 
        self.dll.AUTDGainHoloLM.restype = GainPtr

        self.dll.AUTDGainLMIsDefault.argtypes = [GainPtr]  # type: ignore 
        self.dll.AUTDGainLMIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainHoloNaive.argtypes = [BackendPtr, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_uint64, EmissionConstraintPtr]  # type: ignore 
        self.dll.AUTDGainHoloNaive.restype = GainPtr

        self.dll.AUTDGainNaiveIsDefault.argtypes = [GainPtr]  # type: ignore 
        self.dll.AUTDGainNaiveIsDefault.restype = ctypes.c_bool

        self.dll.AUTDNalgebraBackend.argtypes = [] 
        self.dll.AUTDNalgebraBackend.restype = BackendPtr

        self.dll.AUTDDeleteNalgebraBackend.argtypes = [BackendPtr]  # type: ignore 
        self.dll.AUTDDeleteNalgebraBackend.restype = None

        self.dll.AUTDGainHoloSDP.argtypes = [BackendPtr, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_uint64, ctypes.c_double, ctypes.c_double, ctypes.c_uint32, EmissionConstraintPtr]  # type: ignore 
        self.dll.AUTDGainHoloSDP.restype = GainPtr

        self.dll.AUTDGainSDPIsDefault.argtypes = [GainPtr]  # type: ignore 
        self.dll.AUTDGainSDPIsDefault.restype = ctypes.c_bool

    def gain_holo_constraint_dot_care(self) -> EmissionConstraintPtr:
        return self.dll.AUTDGainHoloConstraintDotCare()

    def gain_holo_constraint_normalize(self) -> EmissionConstraintPtr:
        return self.dll.AUTDGainHoloConstraintNormalize()

    def gain_holo_constraint_uniform(self, intensity: int) -> EmissionConstraintPtr:
        return self.dll.AUTDGainHoloConstraintUniform(intensity)

    def gain_holo_constraint_clamp(self, min_v: int, max_v: int) -> EmissionConstraintPtr:
        return self.dll.AUTDGainHoloConstraintClamp(min_v, max_v)

    def gain_holo_greedy(self, points: ctypes.Array[ctypes.c_double] | None, amps: ctypes.Array[ctypes.c_double] | None, size: int, div: int, constraint: EmissionConstraintPtr) -> GainPtr:
        return self.dll.AUTDGainHoloGreedy(points, amps, size, div, constraint)

    def gain_greedy_is_default(self, greedy: GainPtr) -> ctypes.c_bool:
        return self.dll.AUTDGainGreedyIsDefault(greedy)

    def gain_holo_gs(self, backend: BackendPtr, points: ctypes.Array[ctypes.c_double] | None, amps: ctypes.Array[ctypes.c_double] | None, size: int, repeat: int, constraint: EmissionConstraintPtr) -> GainPtr:
        return self.dll.AUTDGainHoloGS(backend, points, amps, size, repeat, constraint)

    def gain_gs_is_default(self, gs: GainPtr) -> ctypes.c_bool:
        return self.dll.AUTDGainGSIsDefault(gs)

    def gain_holo_gspat(self, backend: BackendPtr, points: ctypes.Array[ctypes.c_double] | None, amps: ctypes.Array[ctypes.c_double] | None, size: int, repeat: int, constraint: EmissionConstraintPtr) -> GainPtr:
        return self.dll.AUTDGainHoloGSPAT(backend, points, amps, size, repeat, constraint)

    def gain_gspat_is_default(self, gs: GainPtr) -> ctypes.c_bool:
        return self.dll.AUTDGainGSPATIsDefault(gs)

    def gain_holo_spl_to_pascal(self, value: float) -> ctypes.c_double:
        return self.dll.AUTDGainHoloSPLToPascal(value)

    def gain_holo_pascal_to_spl(self, value: float) -> ctypes.c_double:
        return self.dll.AUTDGainHoloPascalToSPL(value)

    def gain_holo_lm(self, backend: BackendPtr, points: ctypes.Array[ctypes.c_double] | None, amps: ctypes.Array[ctypes.c_double] | None, size: int, eps_1: float, eps_2: float, tau: float, k_max: int, initial_ptr: ctypes.Array[ctypes.c_double] | None, initial_len: int, constraint: EmissionConstraintPtr) -> GainPtr:
        return self.dll.AUTDGainHoloLM(backend, points, amps, size, eps_1, eps_2, tau, k_max, initial_ptr, initial_len, constraint)

    def gain_lm_is_default(self, gs: GainPtr) -> ctypes.c_bool:
        return self.dll.AUTDGainLMIsDefault(gs)

    def gain_holo_naive(self, backend: BackendPtr, points: ctypes.Array[ctypes.c_double] | None, amps: ctypes.Array[ctypes.c_double] | None, size: int, constraint: EmissionConstraintPtr) -> GainPtr:
        return self.dll.AUTDGainHoloNaive(backend, points, amps, size, constraint)

    def gain_naive_is_default(self, gs: GainPtr) -> ctypes.c_bool:
        return self.dll.AUTDGainNaiveIsDefault(gs)

    def nalgebra_backend(self) -> BackendPtr:
        return self.dll.AUTDNalgebraBackend()

    def delete_nalgebra_backend(self, backend: BackendPtr) -> None:
        return self.dll.AUTDDeleteNalgebraBackend(backend)

    def gain_holo_sdp(self, backend: BackendPtr, points: ctypes.Array[ctypes.c_double] | None, amps: ctypes.Array[ctypes.c_double] | None, size: int, alpha: float, lambda_: float, repeat: int, constraint: EmissionConstraintPtr) -> GainPtr:
        return self.dll.AUTDGainHoloSDP(backend, points, amps, size, alpha, lambda_, repeat, constraint)

    def gain_sdp_is_default(self, gs: GainPtr) -> ctypes.c_bool:
        return self.dll.AUTDGainSDPIsDefault(gs)
