import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3 import DcSysTime
from pyautd3.native_methods.autd3capi_driver import ConstPtr, Duration, GeometryPtr, LinkPtr, ResultStatus
from pyautd3.native_methods.structs import Point3, Quaternion


class RecordPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RecordPtr) and self._fields_ == other._fields_  # pragma: no cover


class InstantRecordOption(ctypes.Structure):
    _fields_ = [
        ("sound_speed", ctypes.c_float),
        ("time_step", Duration),
        ("print_progress", ctypes.c_bool),
        ("memory_limits_hint_mb", ctypes.c_uint64),
        ("gpu", ctypes.c_bool),
    ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, InstantRecordOption) and self._fields_ == other._fields_  # pragma: no cover


class EmulatorPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmulatorPtr) and self._fields_ == other._fields_  # pragma: no cover


class ResultRecord(ctypes.Structure):
    _fields_ = [("result", RecordPtr), ("err_len", ctypes.c_uint32), ("err", ConstPtr)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultRecord) and self._fields_ == other._fields_  # pragma: no cover


class InstantPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, InstantPtr) and self._fields_ == other._fields_  # pragma: no cover


class RmsRecordOption(ctypes.Structure):
    _fields_ = [("sound_speed", ctypes.c_float), ("print_progress", ctypes.c_bool), ("gpu", ctypes.c_bool)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RmsRecordOption) and self._fields_ == other._fields_  # pragma: no cover


class RangeXYZ(ctypes.Structure):
    _fields_ = [
        ("x_start", ctypes.c_float),
        ("x_end", ctypes.c_float),
        ("y_start", ctypes.c_float),
        ("y_end", ctypes.c_float),
        ("z_start", ctypes.c_float),
        ("z_end", ctypes.c_float),
        ("resolution", ctypes.c_float),
    ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RangeXYZ) and self._fields_ == other._fields_  # pragma: no cover


class RmsPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RmsPtr) and self._fields_ == other._fields_  # pragma: no cover


class EmulatorControllerPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmulatorControllerPtr) and self._fields_ == other._fields_  # pragma: no cover


class ResultInstant(ctypes.Structure):
    _fields_ = [("result", InstantPtr), ("err_len", ctypes.c_uint32), ("err", ConstPtr)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultInstant) and self._fields_ == other._fields_  # pragma: no cover


class ResultRms(ctypes.Structure):
    _fields_ = [("result", RmsPtr), ("err_len", ctypes.c_uint32), ("err", ConstPtr)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultRms) and self._fields_ == other._fields_  # pragma: no cover


class Singleton(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:  # pragma: no cover
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):
    def init_dll(self, bin_location: Path, bin_prefix: str, bin_ext: str) -> None:
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi_emulator{bin_ext}"))

        self.dll.AUTDEmulatorRecordDriveCols.argtypes = [RecordPtr]
        self.dll.AUTDEmulatorRecordDriveCols.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorRecordDriveRows.argtypes = [RecordPtr]
        self.dll.AUTDEmulatorRecordDriveRows.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorRecordPhase.argtypes = [RecordPtr, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8))]
        self.dll.AUTDEmulatorRecordPhase.restype = None

        self.dll.AUTDEmulatorRecordPulseWidth.argtypes = [RecordPtr, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8))]
        self.dll.AUTDEmulatorRecordPulseWidth.restype = None

        self.dll.AUTDEmulatorSoundFieldInstant.argtypes = [RecordPtr, RangeXYZ, InstantRecordOption]
        self.dll.AUTDEmulatorSoundFieldInstant.restype = ResultInstant

        self.dll.AUTDEmulatorSoundFieldInstantTimeLen.argtypes = [InstantPtr, Duration]
        self.dll.AUTDEmulatorSoundFieldInstantTimeLen.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorSoundFieldInstantPointsLen.argtypes = [InstantPtr]
        self.dll.AUTDEmulatorSoundFieldInstantPointsLen.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorSoundFieldInstantGetX.argtypes = [InstantPtr, ctypes.POINTER(ctypes.c_float)]
        self.dll.AUTDEmulatorSoundFieldInstantGetX.restype = None

        self.dll.AUTDEmulatorSoundFieldInstantGetY.argtypes = [InstantPtr, ctypes.POINTER(ctypes.c_float)]
        self.dll.AUTDEmulatorSoundFieldInstantGetY.restype = None

        self.dll.AUTDEmulatorSoundFieldInstantGetZ.argtypes = [InstantPtr, ctypes.POINTER(ctypes.c_float)]
        self.dll.AUTDEmulatorSoundFieldInstantGetZ.restype = None

        self.dll.AUTDEmulatorSoundFieldInstantSkip.argtypes = [InstantPtr, Duration]
        self.dll.AUTDEmulatorSoundFieldInstantSkip.restype = ResultStatus

        self.dll.AUTDEmulatorSoundFieldInstantNext.argtypes = [
            InstantPtr,
            Duration,
            ctypes.POINTER(ctypes.c_uint64),
            ctypes.POINTER(ctypes.POINTER(ctypes.c_float)),
        ]
        self.dll.AUTDEmulatorSoundFieldInstantNext.restype = ResultStatus

        self.dll.AUTDEmulatorSoundFieldInstantFree.argtypes = [InstantPtr]
        self.dll.AUTDEmulatorSoundFieldInstantFree.restype = None

        self.dll.AUTDEmulatorTracingInit.argtypes = []
        self.dll.AUTDEmulatorTracingInit.restype = None

        self.dll.AUTDEmulatorTracingInitWithFile.argtypes = [ctypes.c_char_p]
        self.dll.AUTDEmulatorTracingInitWithFile.restype = ResultStatus

        self.dll.AUTDEmulator.argtypes = [ctypes.POINTER(Point3), ctypes.POINTER(Quaternion), ctypes.c_uint16]
        self.dll.AUTDEmulator.restype = EmulatorPtr

        self.dll.AUTDEmulatorFree.argtypes = [EmulatorPtr]
        self.dll.AUTDEmulatorFree.restype = None

        self.dll.AUTDEmulatorGeometry.argtypes = [EmulatorPtr]
        self.dll.AUTDEmulatorGeometry.restype = GeometryPtr

        self.dll.AUTDEmulatorRecordFrom.argtypes = [EmulatorPtr, DcSysTime, ConstPtr]
        self.dll.AUTDEmulatorRecordFrom.restype = ResultRecord

        self.dll.AUTDEmulatorRecordFree.argtypes = [RecordPtr]
        self.dll.AUTDEmulatorRecordFree.restype = None

        self.dll.AUTDEmulatorTickNs.argtypes = [LinkPtr, Duration]
        self.dll.AUTDEmulatorTickNs.restype = ResultStatus

        self.dll.AUTDEmulatorTransducerTableRows.argtypes = [EmulatorPtr]
        self.dll.AUTDEmulatorTransducerTableRows.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorTransducerTable.argtypes = [
            EmulatorPtr,
            ctypes.POINTER(ctypes.c_uint16),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.dll.AUTDEmulatorTransducerTable.restype = None

        self.dll.AUTDEmulatorRecordOutputCols.argtypes = [RecordPtr]
        self.dll.AUTDEmulatorRecordOutputCols.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorRecordOutputVoltage.argtypes = [RecordPtr, ctypes.POINTER(ctypes.POINTER(ctypes.c_float))]
        self.dll.AUTDEmulatorRecordOutputVoltage.restype = None

        self.dll.AUTDEmulatorRecordOutputUltrasound.argtypes = [RecordPtr, ctypes.POINTER(ctypes.POINTER(ctypes.c_float))]
        self.dll.AUTDEmulatorRecordOutputUltrasound.restype = None

        self.dll.AUTDEmulatorSoundFieldRms.argtypes = [RecordPtr, RangeXYZ, RmsRecordOption]
        self.dll.AUTDEmulatorSoundFieldRms.restype = ResultRms

        self.dll.AUTDEmulatorSoundFieldRmsTimeLen.argtypes = [RmsPtr, Duration]
        self.dll.AUTDEmulatorSoundFieldRmsTimeLen.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorSoundFieldRmsPointsLen.argtypes = [RmsPtr]
        self.dll.AUTDEmulatorSoundFieldRmsPointsLen.restype = ctypes.c_uint64

        self.dll.AUTDEmulatorSoundFieldRmsGetX.argtypes = [RmsPtr, ctypes.POINTER(ctypes.c_float)]
        self.dll.AUTDEmulatorSoundFieldRmsGetX.restype = None

        self.dll.AUTDEmulatorSoundFieldRmsGetY.argtypes = [RmsPtr, ctypes.POINTER(ctypes.c_float)]
        self.dll.AUTDEmulatorSoundFieldRmsGetY.restype = None

        self.dll.AUTDEmulatorSoundFieldRmsGetZ.argtypes = [RmsPtr, ctypes.POINTER(ctypes.c_float)]
        self.dll.AUTDEmulatorSoundFieldRmsGetZ.restype = None

        self.dll.AUTDEmulatorSoundFieldRmsSkip.argtypes = [RmsPtr, Duration]
        self.dll.AUTDEmulatorSoundFieldRmsSkip.restype = ResultStatus

        self.dll.AUTDEmulatorSoundFieldRmsNext.argtypes = [
            RmsPtr,
            Duration,
            ctypes.POINTER(ctypes.c_uint64),
            ctypes.POINTER(ctypes.POINTER(ctypes.c_float)),
        ]
        self.dll.AUTDEmulatorSoundFieldRmsNext.restype = ResultStatus

        self.dll.AUTDEmulatorSoundFieldRmsFree.argtypes = [RmsPtr]
        self.dll.AUTDEmulatorSoundFieldRmsFree.restype = None

    def emulator_record_drive_cols(self, record: RecordPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorRecordDriveCols(record)

    def emulator_record_drive_rows(self, record: RecordPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorRecordDriveRows(record)

    def emulator_record_phase(self, record: RecordPtr, time: ctypes.Array[ctypes.c_uint64], v: ctypes.Array[ctypes.Array[ctypes.c_uint8]]) -> None:
        return self.dll.AUTDEmulatorRecordPhase(record, time, v)

    def emulator_record_pulse_width(
        self, record: RecordPtr, time: ctypes.Array[ctypes.c_uint64], v: ctypes.Array[ctypes.Array[ctypes.c_uint8]],
    ) -> None:
        return self.dll.AUTDEmulatorRecordPulseWidth(record, time, v)

    def emulator_sound_field_instant(self, record: RecordPtr, range_: RangeXYZ, option: InstantRecordOption) -> ResultInstant:
        return self.dll.AUTDEmulatorSoundFieldInstant(record, range_, option)

    def emulator_sound_field_instant_time_len(self, sound_field: InstantPtr, duration: Duration) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorSoundFieldInstantTimeLen(sound_field, duration)

    def emulator_sound_field_instant_points_len(self, sound_field: InstantPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorSoundFieldInstantPointsLen(sound_field)

    def emulator_sound_field_instant_get_x(self, sound_field: InstantPtr, x: ctypes.Array[ctypes.c_float]) -> None:
        return self.dll.AUTDEmulatorSoundFieldInstantGetX(sound_field, x)

    def emulator_sound_field_instant_get_y(self, sound_field: InstantPtr, y: ctypes.Array[ctypes.c_float]) -> None:
        return self.dll.AUTDEmulatorSoundFieldInstantGetY(sound_field, y)

    def emulator_sound_field_instant_get_z(self, sound_field: InstantPtr, z: ctypes.Array[ctypes.c_float]) -> None:
        return self.dll.AUTDEmulatorSoundFieldInstantGetZ(sound_field, z)

    def emulator_sound_field_instant_skip(self, sound_field: InstantPtr, duration: Duration) -> ResultStatus:
        return self.dll.AUTDEmulatorSoundFieldInstantSkip(sound_field, duration)

    def emulator_sound_field_instant_next(
        self, sound_field: InstantPtr, duration: Duration, time: ctypes.Array[ctypes.c_uint64], v: ctypes.Array[ctypes.Array[ctypes.c_float]],
    ) -> ResultStatus:
        return self.dll.AUTDEmulatorSoundFieldInstantNext(sound_field, duration, time, v)

    def emulator_sound_field_instant_free(self, sound_field: InstantPtr) -> None:
        return self.dll.AUTDEmulatorSoundFieldInstantFree(sound_field)

    def emulator_tracing_init(self) -> None:
        return self.dll.AUTDEmulatorTracingInit()

    def emulator_tracing_init_with_file(self, path: ctypes.Array[ctypes.c_char]) -> ResultStatus:
        return self.dll.AUTDEmulatorTracingInitWithFile(path)

    def emulator(self, pos: ctypes.Array[Point3], rot: ctypes.Array[Quaternion], len_: int) -> EmulatorPtr:
        return self.dll.AUTDEmulator(pos, rot, len_)

    def emulator_free(self, emulator: EmulatorPtr) -> None:
        return self.dll.AUTDEmulatorFree(emulator)

    def emulator_geometry(self, emulator: EmulatorPtr) -> GeometryPtr:
        return self.dll.AUTDEmulatorGeometry(emulator)

    def emulator_record_from(self, emulator: EmulatorPtr, start_time: DcSysTime, f: ConstPtr) -> ResultRecord:
        return self.dll.AUTDEmulatorRecordFrom(emulator, start_time, f)

    def emulator_record_free(self, record: RecordPtr) -> None:
        return self.dll.AUTDEmulatorRecordFree(record)

    def emulator_tick_ns(self, record: LinkPtr, tick: Duration) -> ResultStatus:
        return self.dll.AUTDEmulatorTickNs(record, tick)

    def emulator_transducer_table_rows(self, emulator: EmulatorPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorTransducerTableRows(emulator)

    def emulator_transducer_table(
        self,
        emulator: EmulatorPtr,
        dev_indices: ctypes.Array[ctypes.c_uint16],
        tr_indices: ctypes.Array[ctypes.c_uint8],
        x: ctypes.Array[ctypes.c_float],
        y: ctypes.Array[ctypes.c_float],
        z: ctypes.Array[ctypes.c_float],
        nx: ctypes.Array[ctypes.c_float],
        ny: ctypes.Array[ctypes.c_float],
        nz: ctypes.Array[ctypes.c_float],
    ) -> None:
        return self.dll.AUTDEmulatorTransducerTable(emulator, dev_indices, tr_indices, x, y, z, nx, ny, nz)

    def emulator_record_output_cols(self, record: RecordPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorRecordOutputCols(record)

    def emulator_record_output_voltage(self, record: RecordPtr, v: ctypes.Array[ctypes.Array[ctypes.c_float]]) -> None:
        return self.dll.AUTDEmulatorRecordOutputVoltage(record, v)

    def emulator_record_output_ultrasound(self, record: RecordPtr, v: ctypes.Array[ctypes.Array[ctypes.c_float]]) -> None:
        return self.dll.AUTDEmulatorRecordOutputUltrasound(record, v)

    def emulator_sound_field_rms(self, record: RecordPtr, range_: RangeXYZ, option: RmsRecordOption) -> ResultRms:
        return self.dll.AUTDEmulatorSoundFieldRms(record, range_, option)

    def emulator_sound_field_rms_time_len(self, sound_field: RmsPtr, duration: Duration) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorSoundFieldRmsTimeLen(sound_field, duration)

    def emulator_sound_field_rms_points_len(self, sound_field: RmsPtr) -> ctypes.c_uint64:
        return self.dll.AUTDEmulatorSoundFieldRmsPointsLen(sound_field)

    def emulator_sound_field_rms_get_x(self, sound_field: RmsPtr, x: ctypes.Array[ctypes.c_float]) -> None:
        return self.dll.AUTDEmulatorSoundFieldRmsGetX(sound_field, x)

    def emulator_sound_field_rms_get_y(self, sound_field: RmsPtr, y: ctypes.Array[ctypes.c_float]) -> None:
        return self.dll.AUTDEmulatorSoundFieldRmsGetY(sound_field, y)

    def emulator_sound_field_rms_get_z(self, sound_field: RmsPtr, z: ctypes.Array[ctypes.c_float]) -> None:
        return self.dll.AUTDEmulatorSoundFieldRmsGetZ(sound_field, z)

    def emulator_sound_field_rms_skip(self, sound_field: RmsPtr, duration: Duration) -> ResultStatus:
        return self.dll.AUTDEmulatorSoundFieldRmsSkip(sound_field, duration)

    def emulator_sound_field_rms_next(
        self, sound_field: RmsPtr, duration: Duration, time: ctypes.Array[ctypes.c_uint64], v: ctypes.Array[ctypes.Array[ctypes.c_float]],
    ) -> ResultStatus:
        return self.dll.AUTDEmulatorSoundFieldRmsNext(sound_field, duration, time, v)

    def emulator_sound_field_rms_free(self, sound_field: RmsPtr) -> None:
        return self.dll.AUTDEmulatorSoundFieldRmsFree(sound_field)
