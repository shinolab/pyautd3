# This file is autogenerated
import threading
import ctypes
import os
from pyautd3.native_methods.structs import Vector3, Quaternion, FfiFuture, LocalFfiFuture, SamplingConfig
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkPtr


class EmulatorControllerPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class EmulatorPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class RecordPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class SoundFieldPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class RecordOption(ctypes.Structure):
    _fields_ = [("sound_speed", ctypes.c_float), ("time_step_ns", ctypes.c_uint64), ("print_progress", ctypes.c_bool), ("memory_limits_hint_mb", ctypes.c_uint64), ("gpu", ctypes.c_bool)]


    def __eq__(self, other: object) -> bool:
        return isinstance(other, RecordOption) and self._fields_ == other._fields_ # pragma: no cover
                    

class Range(ctypes.Structure):
    _fields_ = [("x_start", ctypes.c_float), ("x_end", ctypes.c_float), ("y_start", ctypes.c_float), ("y_end", ctypes.c_float), ("z_start", ctypes.c_float), ("z_end", ctypes.c_float), ("resolution", ctypes.c_float)]


    def __eq__(self, other: object) -> bool:
        return isinstance(other, Range) and self._fields_ == other._fields_ # pragma: no cover
                    

class ResultRecord(ctypes.Structure):
    _fields_ = [("result", RecordPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultRecord) and self._fields_ == other._fields_ # pragma: no cover
                    

class ResultEmualtorErr(ctypes.Structure):
    _fields_ = [("result", ctypes.c_int32), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultEmualtorErr) and self._fields_ == other._fields_ # pragma: no cover
                    

class ResultSoundField(ctypes.Structure):
    _fields_ = [("result", SoundFieldPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultSoundField) and self._fields_ == other._fields_ # pragma: no cover
                    


class Singleton(type):
    _instances = {}  # type: ignore
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances: # pragma: no cover
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):

    def init_dll(self, bin_location: str, bin_prefix: str, bin_ext: str):
        try:
            self.dll = ctypes.CDLL(os.path.join(bin_location, f'{bin_prefix}autd3capi_emulator{bin_ext}'))
        except Exception:   # pragma: no cover
            return          # pragma: no cover

        self.dll.AUTDEmulator.argtypes = [ctypes.POINTER(Vector3), ctypes.POINTER(Quaternion), ctypes.c_uint16]  # type: ignore 
        self.dll.AUTDEmulator.restype = EmulatorPtr

        self.dll.AUTDEmulatorFree.argtypes = [EmulatorPtr]  # type: ignore 
        self.dll.AUTDEmulatorFree.restype = None

        self.dll.AUTDEmulatorWithParallelThreshold.argtypes = [EmulatorPtr, ctypes.c_uint16]  # type: ignore 
        self.dll.AUTDEmulatorWithParallelThreshold.restype = EmulatorPtr

        self.dll.AUTDEmulatorWithSendInterval.argtypes = [EmulatorPtr, ctypes.c_uint64]  # type: ignore 
        self.dll.AUTDEmulatorWithSendInterval.restype = EmulatorPtr

        self.dll.AUTDEmulatorWithReceiveInterval.argtypes = [EmulatorPtr, ctypes.c_uint64]  # type: ignore 
        self.dll.AUTDEmulatorWithReceiveInterval.restype = EmulatorPtr

        self.dll.AUTDEmulatorWithTimerResolution.argtypes = [EmulatorPtr, ctypes.c_uint32]  # type: ignore 
        self.dll.AUTDEmulatorWithTimerResolution.restype = EmulatorPtr

        self.dll.AUTDEmulatorRecordFrom.argtypes = [EmulatorPtr, ctypes.c_uint64, ctypes.c_void_p]  # type: ignore 
        self.dll.AUTDEmulatorRecordFrom.restype = FfiFuture

        self.dll.AUTDEmulatorRecordFree.argtypes = [RecordPtr]  # type: ignore 
        self.dll.AUTDEmulatorRecordFree.restype = None

        self.dll.AUTDEmulatorWaitResultRecord.argtypes = [HandlePtr, FfiFuture]  # type: ignore 
        self.dll.AUTDEmulatorWaitResultRecord.restype = ResultRecord

        self.dll.AUTDEmulatorTickNs.argtypes = [LinkPtr, ctypes.c_uint64]  # type: ignore 
        self.dll.AUTDEmulatorTickNs.restype = ResultEmualtorErr

        self.dll.AUTDEmulatorRecordNumDevices.argtypes = [RecordPtr]  # type: ignore 
        self.dll.AUTDEmulatorRecordNumDevices.restype = ctypes.c_uint16

        self.dll.AUTDEmulatorRecordNumTransducers.argtypes = [RecordPtr, ctypes.c_uint16]  # type: ignore 
        self.dll.AUTDEmulatorRecordNumTransducers.restype = ctypes.c_uint8

        self.dll.AUTDEmulatorRecordDriveLen.argtypes = [RecordPtr]  # type: ignore 
        self.dll.AUTDEmulatorRecordDriveLen.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorRecordDriveTime.argtypes = [RecordPtr, ctypes.POINTER(ctypes.c_float)]  # type: ignore 
        self.dll.AUTDEmulatorRecordDriveTime.restype = None

        self.dll.AUTDEmulatorRecordDrivePulseWidth.argtypes = [RecordPtr, ctypes.c_uint16, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint8)]  # type: ignore 
        self.dll.AUTDEmulatorRecordDrivePulseWidth.restype = None

        self.dll.AUTDEmulatorRecordDrivePhase.argtypes = [RecordPtr, ctypes.c_uint16, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint8)]  # type: ignore 
        self.dll.AUTDEmulatorRecordDrivePhase.restype = None

        self.dll.AUTDEmulatorRecordOutputLen.argtypes = [RecordPtr]  # type: ignore 
        self.dll.AUTDEmulatorRecordOutputLen.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorRecordOutputTime.argtypes = [RecordPtr, ctypes.POINTER(ctypes.c_float)]  # type: ignore 
        self.dll.AUTDEmulatorRecordOutputTime.restype = None

        self.dll.AUTDEmulatorRecordOutputVoltage.argtypes = [RecordPtr, ctypes.c_uint16, ctypes.c_uint8, ctypes.POINTER(ctypes.c_float)]  # type: ignore 
        self.dll.AUTDEmulatorRecordOutputVoltage.restype = None

        self.dll.AUTDEmulatorRecordOutputUltrasound.argtypes = [RecordPtr, ctypes.c_uint16, ctypes.c_uint8, ctypes.POINTER(ctypes.c_float)]  # type: ignore 
        self.dll.AUTDEmulatorRecordOutputUltrasound.restype = None

        self.dll.AUTDEmulatorSoundField.argtypes = [RecordPtr, Range, RecordOption]  # type: ignore 
        self.dll.AUTDEmulatorSoundField.restype = LocalFfiFuture

        self.dll.AUTDEmulatorWaitSoundField.argtypes = [HandlePtr, LocalFfiFuture]  # type: ignore 
        self.dll.AUTDEmulatorWaitSoundField.restype = ResultSoundField

        self.dll.AUTDEmulatorSoundFieldTimeLen.argtypes = [SoundFieldPtr, ctypes.c_uint64]  # type: ignore 
        self.dll.AUTDEmulatorSoundFieldTimeLen.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorSoundFieldPointsLen.argtypes = [SoundFieldPtr]  # type: ignore 
        self.dll.AUTDEmulatorSoundFieldPointsLen.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorSoundFieldNext.argtypes = [SoundFieldPtr, ctypes.c_uint64, ctypes.c_bool, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.POINTER(ctypes.c_float))]  # type: ignore 
        self.dll.AUTDEmulatorSoundFieldNext.restype = FfiFuture

        self.dll.AUTDEmulatorWaitResultEmualtorErr.argtypes = [HandlePtr, FfiFuture]  # type: ignore 
        self.dll.AUTDEmulatorWaitResultEmualtorErr.restype = ResultEmualtorErr

        self.dll.AUTDEmulatorSoundFieldFree.argtypes = [SoundFieldPtr]  # type: ignore 
        self.dll.AUTDEmulatorSoundFieldFree.restype = None

    def emulator(self, pos: ctypes.Array | None, rot: ctypes.Array | None, len: int) -> EmulatorPtr:
        return self.dll.AUTDEmulator(pos, rot, len)

    def emulator_free(self, emulator: EmulatorPtr) -> None:
        return self.dll.AUTDEmulatorFree(emulator)

    def emulator_with_parallel_threshold(self, emulator: EmulatorPtr, parallel_threshold: int) -> EmulatorPtr:
        return self.dll.AUTDEmulatorWithParallelThreshold(emulator, parallel_threshold)

    def emulator_with_send_interval(self, emulator: EmulatorPtr, interval_ns: int) -> EmulatorPtr:
        return self.dll.AUTDEmulatorWithSendInterval(emulator, interval_ns)

    def emulator_with_receive_interval(self, emulator: EmulatorPtr, interval_ns: int) -> EmulatorPtr:
        return self.dll.AUTDEmulatorWithReceiveInterval(emulator, interval_ns)

    def emulator_with_timer_resolution(self, emulator: EmulatorPtr, resolution: int) -> EmulatorPtr:
        return self.dll.AUTDEmulatorWithTimerResolution(emulator, resolution)

    def emulator_record_from(self, emulator: EmulatorPtr, start_time: int, f: ctypes.c_void_p | None) -> FfiFuture:
        return self.dll.AUTDEmulatorRecordFrom(emulator, start_time, f)

    def emulator_record_free(self, record: RecordPtr) -> None:
        return self.dll.AUTDEmulatorRecordFree(record)

    def emulator_wait_result_record(self, handle: HandlePtr, future: FfiFuture) -> ResultRecord:
        return self.dll.AUTDEmulatorWaitResultRecord(handle, future)

    def emulator_tick_ns(self, record: LinkPtr, tick_ns: int) -> ResultEmualtorErr:
        return self.dll.AUTDEmulatorTickNs(record, tick_ns)

    def emulator_record_num_devices(self, record: RecordPtr) -> ctypes.c_uint16:
        return self.dll.AUTDEmulatorRecordNumDevices(record)

    def emulator_record_num_transducers(self, record: RecordPtr, dev_idx: int) -> ctypes.c_uint8:
        return self.dll.AUTDEmulatorRecordNumTransducers(record, dev_idx)

    def emulator_record_drive_len(self, record: RecordPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorRecordDriveLen(record)

    def emulator_record_drive_time(self, record: RecordPtr, time: ctypes.Array[ctypes.c_float] | None) -> None:
        return self.dll.AUTDEmulatorRecordDriveTime(record, time)

    def emulator_record_drive_pulse_width(self, record: RecordPtr, dev_idx: int, tr_idx: int, pulsewidth: ctypes.Array[ctypes.c_uint8] | None) -> None:
        return self.dll.AUTDEmulatorRecordDrivePulseWidth(record, dev_idx, tr_idx, pulsewidth)

    def emulator_record_drive_phase(self, record: RecordPtr, dev_idx: int, tr_idx: int, pulsewidth: ctypes.Array[ctypes.c_uint8] | None) -> None:
        return self.dll.AUTDEmulatorRecordDrivePhase(record, dev_idx, tr_idx, pulsewidth)

    def emulator_record_output_len(self, record: RecordPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorRecordOutputLen(record)

    def emulator_record_output_time(self, record: RecordPtr, time: ctypes.Array[ctypes.c_float] | None) -> None:
        return self.dll.AUTDEmulatorRecordOutputTime(record, time)

    def emulator_record_output_voltage(self, record: RecordPtr, dev_idx: int, tr_idx: int, v: ctypes.Array[ctypes.c_float] | None) -> None:
        return self.dll.AUTDEmulatorRecordOutputVoltage(record, dev_idx, tr_idx, v)

    def emulator_record_output_ultrasound(self, record: RecordPtr, dev_idx: int, tr_idx: int, v: ctypes.Array[ctypes.c_float] | None) -> None:
        return self.dll.AUTDEmulatorRecordOutputUltrasound(record, dev_idx, tr_idx, v)

    def emulator_sound_field(self, record: RecordPtr, range: Range, option: RecordOption) -> LocalFfiFuture:
        return self.dll.AUTDEmulatorSoundField(record, range, option)

    def emulator_wait_sound_field(self, handle: HandlePtr, future: LocalFfiFuture) -> ResultSoundField:
        return self.dll.AUTDEmulatorWaitSoundField(handle, future)

    def emulator_sound_field_time_len(self, sound_field: SoundFieldPtr, duration_ns: int) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorSoundFieldTimeLen(sound_field, duration_ns)

    def emulator_sound_field_points_len(self, sound_field: SoundFieldPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorSoundFieldPointsLen(sound_field)

    def emulator_sound_field_next(self, sound_field: SoundFieldPtr, duration_ns: int, skip: bool, time: ctypes.Array[ctypes.c_float] | None, v: ctypes.Array[ctypes.Array[ctypes.c_float]]) -> FfiFuture:
        return self.dll.AUTDEmulatorSoundFieldNext(sound_field, duration_ns, skip, time, v)

    def emulator_wait_result_emualtor_err(self, handle: HandlePtr, future: FfiFuture) -> ResultEmualtorErr:
        return self.dll.AUTDEmulatorWaitResultEmualtorErr(handle, future)

    def emulator_sound_field_free(self, sound_field: SoundFieldPtr) -> None:
        return self.dll.AUTDEmulatorSoundFieldFree(sound_field)
