import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3 import (
    Angle,
    BesselOption,
    DcSysTime,
    Drive,
    FixedCompletionSteps,
    FixedUpdateRate,
    FocusOption,
    GainSTMOption,
    GPIOIn,
    Intensity,
    Phase,
    PlaneOption,
    Segment,
)
from pyautd3.native_methods.autd3capi_driver import (
    ControllerPtr,
    DatagramPtr,
    DevicePtr,
    Duration,
    EnvironmentPtr,
    FociSTMPtr,
    GainPtr,
    GainSTMPtr,
    GeometryPtr,
    GPIOOutputTypeWrap,
    LinkPtr,
    LoopBehavior,
    ModulationPtr,
    OptionDuration,
    ResultDuration,
    ResultF32,
    ResultSamplingConfig,
    ResultStatus,
    ResultU8,
    ResultU16,
    SamplingConfigWrap,
    SenderPtr,
    TimerStrategyWrap,
    TransducerPtr,
    TransitionModeWrap,
)
from pyautd3.native_methods.structs import Point3, Quaternion, Vector3


class FPGAStateListPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FPGAStateListPtr) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class FirmwareVersionListPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FirmwareVersionListPtr) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class FixedCompletionTime(ctypes.Structure):
    _fields_ = [("intensity", Duration), ("phase", Duration), ("strict", ctypes.c_bool)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FixedCompletionTime) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class FourierOption(ctypes.Structure):
    _fields_ = [("has_scale_factor", ctypes.c_bool), ("scale_factor", ctypes.c_float), ("clamp", ctypes.c_bool), ("offset", ctypes.c_uint8)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FourierOption) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class GroupGainMapPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GroupGainMapPtr) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class ResultController(ctypes.Structure):
    _fields_ = [("result", ControllerPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultController) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class ResultFPGAStateList(ctypes.Structure):
    _fields_ = [("result", FPGAStateListPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultFPGAStateList) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class ResultFirmwareVersionList(ctypes.Structure):
    _fields_ = [("result", FirmwareVersionListPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultFirmwareVersionList) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class SenderOption(ctypes.Structure):
    _fields_ = [
        ("send_interval", Duration),
        ("receive_interval", Duration),
        ("timeout", OptionDuration),
        ("parallel", ctypes.c_uint8),
        ("strict", ctypes.c_bool),
    ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SenderOption) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class SineOption(ctypes.Structure):
    _fields_ = [
        ("intensity", ctypes.c_uint8),
        ("offset", ctypes.c_uint8),
        ("phase", Angle),
        ("clamp", ctypes.c_bool),
        ("sampling_config_div", ctypes.c_uint16),
    ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SineOption) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class SquareOption(ctypes.Structure):
    _fields_ = [("low", ctypes.c_uint8), ("high", ctypes.c_uint8), ("duty", ctypes.c_float), ("sampling_config_div", ctypes.c_uint16)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SquareOption) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


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
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi{bin_ext}"))

        self.dll.AUTDControllerOpen.argtypes = [
            ctypes.POINTER(Point3),
            ctypes.POINTER(Quaternion),
            ctypes.c_uint16,
            LinkPtr,
            SenderOption,
            TimerStrategyWrap,
        ]
        self.dll.AUTDControllerOpen.restype = ResultController

        self.dll.AUTDControllerClose.argtypes = [ControllerPtr]
        self.dll.AUTDControllerClose.restype = ResultStatus

        self.dll.AUTDControllerFPGAState.argtypes = [ControllerPtr]
        self.dll.AUTDControllerFPGAState.restype = ResultFPGAStateList

        self.dll.AUTDControllerFPGAStateGet.argtypes = [FPGAStateListPtr, ctypes.c_uint32]
        self.dll.AUTDControllerFPGAStateGet.restype = ctypes.c_int16

        self.dll.AUTDControllerFPGAStateDelete.argtypes = [FPGAStateListPtr]
        self.dll.AUTDControllerFPGAStateDelete.restype = None

        self.dll.AUTDControllerFirmwareVersionListPointer.argtypes = [ControllerPtr]
        self.dll.AUTDControllerFirmwareVersionListPointer.restype = ResultFirmwareVersionList

        self.dll.AUTDControllerFirmwareVersionGet.argtypes = [FirmwareVersionListPtr, ctypes.c_uint32, ctypes.c_char_p]
        self.dll.AUTDControllerFirmwareVersionGet.restype = None

        self.dll.AUTDControllerFirmwareVersionListPointerDelete.argtypes = [FirmwareVersionListPtr]
        self.dll.AUTDControllerFirmwareVersionListPointerDelete.restype = None

        self.dll.AUTDFirmwareLatest.argtypes = [ctypes.c_char_p]
        self.dll.AUTDFirmwareLatest.restype = None

        self.dll.AUTDSetDefaultSenderOption.argtypes = [ControllerPtr, SenderOption]
        self.dll.AUTDSetDefaultSenderOption.restype = None

        self.dll.AUTDSender.argtypes = [ControllerPtr, SenderOption, TimerStrategyWrap]
        self.dll.AUTDSender.restype = SenderPtr

        self.dll.AUTDSenderSend.argtypes = [SenderPtr, DatagramPtr]
        self.dll.AUTDSenderSend.restype = ResultStatus

        self.dll.AUTDSpinSleepDefaultAccuracy.argtypes = []
        self.dll.AUTDSpinSleepDefaultAccuracy.restype = ctypes.c_uint32

        self.dll.AUTDSenderOptionIsDefault.argtypes = [SenderOption]
        self.dll.AUTDSenderOptionIsDefault.restype = ctypes.c_bool

        self.dll.AUTDDatagramClear.argtypes = []
        self.dll.AUTDDatagramClear.restype = DatagramPtr

        self.dll.AUTDDatagramForceFan.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr]
        self.dll.AUTDDatagramForceFan.restype = DatagramPtr

        self.dll.AUTDDatagramGPIOOutputs.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr]
        self.dll.AUTDDatagramGPIOOutputs.restype = DatagramPtr

        self.dll.AUTDDatagramGroup.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            GeometryPtr,
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(DatagramPtr),
            ctypes.c_uint16,
        ]
        self.dll.AUTDDatagramGroup.restype = DatagramPtr

        self.dll.AUTDDatagramOutputMask.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr]
        self.dll.AUTDDatagramOutputMask.restype = DatagramPtr

        self.dll.AUTDDatagramOutputMaskWithSegment.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr, ctypes.c_uint8]
        self.dll.AUTDDatagramOutputMaskWithSegment.restype = DatagramPtr

        self.dll.AUTDDatagramPhaseCorr.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr]
        self.dll.AUTDDatagramPhaseCorr.restype = DatagramPtr

        self.dll.AUTDDatagramPulseWidthEncoder256.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr]
        self.dll.AUTDDatagramPulseWidthEncoder256.restype = DatagramPtr

        self.dll.AUTDDatagramPulseWidthEncoder256Default.argtypes = []
        self.dll.AUTDDatagramPulseWidthEncoder256Default.restype = DatagramPtr

        self.dll.AUTDDatagramPulseWidthEncoder512.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr]
        self.dll.AUTDDatagramPulseWidthEncoder512.restype = DatagramPtr

        self.dll.AUTDDatagramPulseWidthEncoder512Default.argtypes = []
        self.dll.AUTDDatagramPulseWidthEncoder512Default.restype = DatagramPtr

        self.dll.AUTDDatagramReadsFPGAState.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr]
        self.dll.AUTDDatagramReadsFPGAState.restype = DatagramPtr

        self.dll.AUTDDatagramSwapSegmentModulation.argtypes = [ctypes.c_uint8, TransitionModeWrap]
        self.dll.AUTDDatagramSwapSegmentModulation.restype = DatagramPtr

        self.dll.AUTDDatagramSwapSegmentFociSTM.argtypes = [ctypes.c_uint8, TransitionModeWrap]
        self.dll.AUTDDatagramSwapSegmentFociSTM.restype = DatagramPtr

        self.dll.AUTDDatagramSwapSegmentGainSTM.argtypes = [ctypes.c_uint8, TransitionModeWrap]
        self.dll.AUTDDatagramSwapSegmentGainSTM.restype = DatagramPtr

        self.dll.AUTDDatagramSwapSegmentGain.argtypes = [ctypes.c_uint8, TransitionModeWrap]
        self.dll.AUTDDatagramSwapSegmentGain.restype = DatagramPtr

        self.dll.AUTDDatagramSilencerFromUpdateRate.argtypes = [FixedUpdateRate]
        self.dll.AUTDDatagramSilencerFromUpdateRate.restype = DatagramPtr

        self.dll.AUTDDatagramSilencerFromCompletionSteps.argtypes = [FixedCompletionSteps]
        self.dll.AUTDDatagramSilencerFromCompletionSteps.restype = DatagramPtr

        self.dll.AUTDDatagramSilencerFromCompletionTime.argtypes = [FixedCompletionTime]
        self.dll.AUTDDatagramSilencerFromCompletionTime.restype = DatagramPtr

        self.dll.AUTDDatagramSilencerFixedCompletionStepsIsDefault.argtypes = [FixedCompletionSteps]
        self.dll.AUTDDatagramSilencerFixedCompletionStepsIsDefault.restype = ctypes.c_bool

        self.dll.AUTDSTMFoci.argtypes = [SamplingConfigWrap, ctypes.c_void_p, ctypes.c_uint16, ctypes.c_uint8]
        self.dll.AUTDSTMFoci.restype = FociSTMPtr

        self.dll.AUTDSTMFociIntoDatagramWithSegment.argtypes = [FociSTMPtr, ctypes.c_uint8, ctypes.c_uint8, TransitionModeWrap]
        self.dll.AUTDSTMFociIntoDatagramWithSegment.restype = DatagramPtr

        self.dll.AUTDSTMFociIntoDatagramWithLoopBehavior.argtypes = [FociSTMPtr, ctypes.c_uint8, ctypes.c_uint8, TransitionModeWrap, LoopBehavior]
        self.dll.AUTDSTMFociIntoDatagramWithLoopBehavior.restype = DatagramPtr

        self.dll.AUTDSTMFociIntoDatagram.argtypes = [FociSTMPtr, ctypes.c_uint8]
        self.dll.AUTDSTMFociIntoDatagram.restype = DatagramPtr

        self.dll.AUTDSTMGain.argtypes = [SamplingConfigWrap, ctypes.POINTER(GainPtr), ctypes.c_uint16, GainSTMOption]
        self.dll.AUTDSTMGain.restype = GainSTMPtr

        self.dll.AUTDSTMGainIntoDatagramWithSegment.argtypes = [GainSTMPtr, ctypes.c_uint8, TransitionModeWrap]
        self.dll.AUTDSTMGainIntoDatagramWithSegment.restype = DatagramPtr

        self.dll.AUTDSTMGainIntoDatagramWithLoopBehavior.argtypes = [GainSTMPtr, ctypes.c_uint8, TransitionModeWrap, LoopBehavior]
        self.dll.AUTDSTMGainIntoDatagramWithLoopBehavior.restype = DatagramPtr

        self.dll.AUTDSTMGainIntoDatagram.argtypes = [GainSTMPtr]
        self.dll.AUTDSTMGainIntoDatagram.restype = DatagramPtr

        self.dll.AUTDSTMConfigFromFreq.argtypes = [ctypes.c_float, ctypes.c_uint16]
        self.dll.AUTDSTMConfigFromFreq.restype = ResultSamplingConfig

        self.dll.AUTDSTMConfigFromPeriod.argtypes = [Duration, ctypes.c_uint16]
        self.dll.AUTDSTMConfigFromPeriod.restype = ResultSamplingConfig

        self.dll.AUTDSTMConfigFromFreqNearest.argtypes = [ctypes.c_float, ctypes.c_uint16]
        self.dll.AUTDSTMConfigFromFreqNearest.restype = SamplingConfigWrap

        self.dll.AUTDSTMConfigFromPeriodNearest.argtypes = [Duration, ctypes.c_uint16]
        self.dll.AUTDSTMConfigFromPeriodNearest.restype = SamplingConfigWrap

        self.dll.AUTDDatagramSynchronize.argtypes = []
        self.dll.AUTDDatagramSynchronize.restype = DatagramPtr

        self.dll.AUTDDatagramTuple.argtypes = [DatagramPtr, DatagramPtr]
        self.dll.AUTDDatagramTuple.restype = DatagramPtr

        self.dll.AUTDDcSysTimeNow.argtypes = []
        self.dll.AUTDDcSysTimeNow.restype = DcSysTime

        self.dll.AUTDGPIOOutputTypeNone.argtypes = []
        self.dll.AUTDGPIOOutputTypeNone.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeBaseSignal.argtypes = []
        self.dll.AUTDGPIOOutputTypeBaseSignal.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeThermo.argtypes = []
        self.dll.AUTDGPIOOutputTypeThermo.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeForceFan.argtypes = []
        self.dll.AUTDGPIOOutputTypeForceFan.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeSync.argtypes = []
        self.dll.AUTDGPIOOutputTypeSync.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeModSegment.argtypes = []
        self.dll.AUTDGPIOOutputTypeModSegment.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeModIdx.argtypes = [ctypes.c_uint16]
        self.dll.AUTDGPIOOutputTypeModIdx.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeStmSegment.argtypes = []
        self.dll.AUTDGPIOOutputTypeStmSegment.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeStmIdx.argtypes = [ctypes.c_uint16]
        self.dll.AUTDGPIOOutputTypeStmIdx.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeIsStmMode.argtypes = []
        self.dll.AUTDGPIOOutputTypeIsStmMode.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypePwmOut.argtypes = [TransducerPtr]
        self.dll.AUTDGPIOOutputTypePwmOut.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeDirect.argtypes = [ctypes.c_bool]
        self.dll.AUTDGPIOOutputTypeDirect.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeSysTimeEq.argtypes = [DcSysTime]
        self.dll.AUTDGPIOOutputTypeSysTimeEq.restype = GPIOOutputTypeWrap

        self.dll.AUTDGPIOOutputTypeSyncDiff.argtypes = []
        self.dll.AUTDGPIOOutputTypeSyncDiff.restype = GPIOOutputTypeWrap

        self.dll.AUTDLoopBehaviorInfinite.argtypes = []
        self.dll.AUTDLoopBehaviorInfinite.restype = LoopBehavior

        self.dll.AUTDLoopBehaviorFinite.argtypes = [ctypes.c_uint16]
        self.dll.AUTDLoopBehaviorFinite.restype = LoopBehavior

        self.dll.AUTDPhaseFromRad.argtypes = [ctypes.c_float]
        self.dll.AUTDPhaseFromRad.restype = ctypes.c_uint8

        self.dll.AUTDPhaseToRad.argtypes = [Phase]
        self.dll.AUTDPhaseToRad.restype = ctypes.c_float

        self.dll.AUTDPulseWidth256.argtypes = [ctypes.c_uint8]
        self.dll.AUTDPulseWidth256.restype = ResultU8

        self.dll.AUTDPulseWidth512.argtypes = [ctypes.c_uint16]
        self.dll.AUTDPulseWidth512.restype = ResultU16

        self.dll.AUTDPulseWidth256FromDuty.argtypes = [ctypes.c_float]
        self.dll.AUTDPulseWidth256FromDuty.restype = ResultU8

        self.dll.AUTDPulseWidth512FromDuty.argtypes = [ctypes.c_float]
        self.dll.AUTDPulseWidth512FromDuty.restype = ResultU16

        self.dll.AUTDSamplingConfigFromDivide.argtypes = [ctypes.c_uint16]
        self.dll.AUTDSamplingConfigFromDivide.restype = ResultSamplingConfig

        self.dll.AUTDSamplingConfigFromFreq.argtypes = [ctypes.c_float]
        self.dll.AUTDSamplingConfigFromFreq.restype = SamplingConfigWrap

        self.dll.AUTDSamplingConfigFromPeriod.argtypes = [Duration]
        self.dll.AUTDSamplingConfigFromPeriod.restype = SamplingConfigWrap

        self.dll.AUTDSamplingConfigIntoNearest.argtypes = [SamplingConfigWrap]
        self.dll.AUTDSamplingConfigIntoNearest.restype = SamplingConfigWrap

        self.dll.AUTDSamplingConfigDivide.argtypes = [SamplingConfigWrap]
        self.dll.AUTDSamplingConfigDivide.restype = ResultU16

        self.dll.AUTDSamplingConfigFreq.argtypes = [SamplingConfigWrap]
        self.dll.AUTDSamplingConfigFreq.restype = ResultF32

        self.dll.AUTDSamplingConfigPeriod.argtypes = [SamplingConfigWrap]
        self.dll.AUTDSamplingConfigPeriod.restype = ResultDuration

        self.dll.AUTDSamplingConfigEq.argtypes = [SamplingConfigWrap, SamplingConfigWrap]
        self.dll.AUTDSamplingConfigEq.restype = ctypes.c_bool

        self.dll.AUTDTransitionModeSyncIdx.argtypes = []
        self.dll.AUTDTransitionModeSyncIdx.restype = TransitionModeWrap

        self.dll.AUTDTransitionModeSysTime.argtypes = [DcSysTime]
        self.dll.AUTDTransitionModeSysTime.restype = TransitionModeWrap

        self.dll.AUTDTransitionModeGPIO.argtypes = [ctypes.c_uint8]
        self.dll.AUTDTransitionModeGPIO.restype = TransitionModeWrap

        self.dll.AUTDTransitionModeExt.argtypes = []
        self.dll.AUTDTransitionModeExt.restype = TransitionModeWrap

        self.dll.AUTDTransitionModeImmediate.argtypes = []
        self.dll.AUTDTransitionModeImmediate.restype = TransitionModeWrap

        self.dll.AUTDTransitionModeNone.argtypes = []
        self.dll.AUTDTransitionModeNone.restype = TransitionModeWrap

        self.dll.AUTDEnvironment.argtypes = [ControllerPtr]
        self.dll.AUTDEnvironment.restype = EnvironmentPtr

        self.dll.AUTDEnvironmentGetSoundSpeed.argtypes = [EnvironmentPtr]
        self.dll.AUTDEnvironmentGetSoundSpeed.restype = ctypes.c_float

        self.dll.AUTDEnvironmentSetSoundSpeed.argtypes = [EnvironmentPtr, ctypes.c_float]
        self.dll.AUTDEnvironmentSetSoundSpeed.restype = None

        self.dll.AUTDEnvironmentSetSoundSpeedFromTemp.argtypes = [EnvironmentPtr, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
        self.dll.AUTDEnvironmentSetSoundSpeedFromTemp.restype = None

        self.dll.AUTDEnvironmentWavelength.argtypes = [EnvironmentPtr]
        self.dll.AUTDEnvironmentWavelength.restype = ctypes.c_float

        self.dll.AUTDEnvironmentWavenumber.argtypes = [EnvironmentPtr]
        self.dll.AUTDEnvironmentWavenumber.restype = ctypes.c_float

        self.dll.AUTDGainBessel.argtypes = [Point3, Vector3, Angle, BesselOption]
        self.dll.AUTDGainBessel.restype = GainPtr

        self.dll.AUTDGainBesselIsDefault.argtypes = [BesselOption]
        self.dll.AUTDGainBesselIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainCustom.argtypes = [ctypes.c_void_p, ctypes.c_void_p, GeometryPtr]
        self.dll.AUTDGainCustom.restype = GainPtr

        self.dll.AUTDGainFocus.argtypes = [Point3, FocusOption]
        self.dll.AUTDGainFocus.restype = GainPtr

        self.dll.AUTDGainFocusIsDefault.argtypes = [FocusOption]
        self.dll.AUTDGainFocusIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainGroupCreateMap.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.c_uint16]
        self.dll.AUTDGainGroupCreateMap.restype = GroupGainMapPtr

        self.dll.AUTDGainGroupMapSet.argtypes = [GroupGainMapPtr, ctypes.c_uint16, ctypes.POINTER(ctypes.c_int32)]
        self.dll.AUTDGainGroupMapSet.restype = GroupGainMapPtr

        self.dll.AUTDGainGroup.argtypes = [GroupGainMapPtr, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(GainPtr), ctypes.c_uint32]
        self.dll.AUTDGainGroup.restype = GainPtr

        self.dll.AUTDGainIntoDatagramWithSegment.argtypes = [GainPtr, ctypes.c_uint8, TransitionModeWrap]
        self.dll.AUTDGainIntoDatagramWithSegment.restype = DatagramPtr

        self.dll.AUTDGainIntoDatagram.argtypes = [GainPtr]
        self.dll.AUTDGainIntoDatagram.restype = DatagramPtr

        self.dll.AUTDGainNull.argtypes = []
        self.dll.AUTDGainNull.restype = GainPtr

        self.dll.AUTDGainPlane.argtypes = [Vector3, PlaneOption]
        self.dll.AUTDGainPlane.restype = GainPtr

        self.dll.AUTDGainPlanelIsDefault.argtypes = [PlaneOption]
        self.dll.AUTDGainPlanelIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGainUniform.argtypes = [Intensity, Phase]
        self.dll.AUTDGainUniform.restype = GainPtr

        self.dll.AUTDDevice.argtypes = [GeometryPtr, ctypes.c_uint16]
        self.dll.AUTDDevice.restype = DevicePtr

        self.dll.AUTDDeviceNumTransducers.argtypes = [DevicePtr]
        self.dll.AUTDDeviceNumTransducers.restype = ctypes.c_uint32

        self.dll.AUTDDeviceCenter.argtypes = [DevicePtr]
        self.dll.AUTDDeviceCenter.restype = Point3

        self.dll.AUTDDeviceRotation.argtypes = [DevicePtr]
        self.dll.AUTDDeviceRotation.restype = Quaternion

        self.dll.AUTDDeviceDirectionX.argtypes = [DevicePtr]
        self.dll.AUTDDeviceDirectionX.restype = Vector3

        self.dll.AUTDDeviceDirectionY.argtypes = [DevicePtr]
        self.dll.AUTDDeviceDirectionY.restype = Vector3

        self.dll.AUTDDeviceDirectionAxial.argtypes = [DevicePtr]
        self.dll.AUTDDeviceDirectionAxial.restype = Vector3

        self.dll.AUTDGeometry.argtypes = [ControllerPtr]
        self.dll.AUTDGeometry.restype = GeometryPtr

        self.dll.AUTDGeometryNumDevices.argtypes = [GeometryPtr]
        self.dll.AUTDGeometryNumDevices.restype = ctypes.c_uint32

        self.dll.AUTDGeometryNumTransducers.argtypes = [GeometryPtr]
        self.dll.AUTDGeometryNumTransducers.restype = ctypes.c_uint32

        self.dll.AUTDGeometrCenter.argtypes = [GeometryPtr]
        self.dll.AUTDGeometrCenter.restype = Point3

        self.dll.AUTDGeometryReconfigure.argtypes = [GeometryPtr, ctypes.POINTER(Point3), ctypes.POINTER(Quaternion)]
        self.dll.AUTDGeometryReconfigure.restype = None

        self.dll.AUTDRotationFromEulerXYZ.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float]
        self.dll.AUTDRotationFromEulerXYZ.restype = Quaternion

        self.dll.AUTDRotationFromEulerZYZ.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float]
        self.dll.AUTDRotationFromEulerZYZ.restype = Quaternion

        self.dll.AUTDTransducer.argtypes = [DevicePtr, ctypes.c_uint8]
        self.dll.AUTDTransducer.restype = TransducerPtr

        self.dll.AUTDTransducerPosition.argtypes = [TransducerPtr]
        self.dll.AUTDTransducerPosition.restype = Point3

        self.dll.AUTDLinkAudit.argtypes = []
        self.dll.AUTDLinkAudit.restype = LinkPtr

        self.dll.AUTDLinkAuditIsOpen.argtypes = [LinkPtr]
        self.dll.AUTDLinkAuditIsOpen.restype = ctypes.c_bool

        self.dll.AUTDLinkAuditBreakDown.argtypes = [LinkPtr]
        self.dll.AUTDLinkAuditBreakDown.restype = None

        self.dll.AUTDLinkAuditRepair.argtypes = [LinkPtr]
        self.dll.AUTDLinkAuditRepair.restype = None

        self.dll.AUTDLinkAuditCpuNumTransducers.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditCpuNumTransducers.restype = ctypes.c_uint32

        self.dll.AUTDLinkAuditFpgaAssertThermalSensor.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaAssertThermalSensor.restype = None

        self.dll.AUTDLinkAuditFpgaDeassertThermalSensor.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaDeassertThermalSensor.restype = None

        self.dll.AUTDLinkAuditFpgaIsForceFan.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaIsForceFan.restype = ctypes.c_bool

        self.dll.AUTDLinkAuditFpgaCurrentStmSegment.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaCurrentStmSegment.restype = Segment

        self.dll.AUTDLinkAuditFpgaCurrentModSegment.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaCurrentModSegment.restype = Segment

        self.dll.AUTDLinkAuditFpgaIsStmGainMode.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaIsStmGainMode.restype = ctypes.c_bool

        self.dll.AUTDLinkAuditCpuSilencerStrict.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditCpuSilencerStrict.restype = ctypes.c_bool

        self.dll.AUTDLinkAuditFpgaSilencerUpdateRateIntensity.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaSilencerUpdateRateIntensity.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaSilencerUpdateRatePhase.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaSilencerUpdateRatePhase.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaSilencerCompletionStepsIntensity.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaSilencerCompletionStepsIntensity.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaSilencerCompletionStepsPhase.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaSilencerCompletionStepsPhase.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaSilencerFixedCompletionStepsMode.argtypes = [LinkPtr, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaSilencerFixedCompletionStepsMode.restype = ctypes.c_bool

        self.dll.AUTDLinkAuditFpgaGPIOOutputTypes.argtypes = [LinkPtr, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8)]
        self.dll.AUTDLinkAuditFpgaGPIOOutputTypes.restype = None

        self.dll.AUTDLinkAuditFpgaDebugValues.argtypes = [LinkPtr, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint64)]
        self.dll.AUTDLinkAuditFpgaDebugValues.restype = None

        self.dll.AUTDLinkAuditFpgaStmFreqDivide.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaStmFreqDivide.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaStmCycle.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaStmCycle.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaSoundSpeed.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaSoundSpeed.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaStmLoopBehavior.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaStmLoopBehavior.restype = LoopBehavior

        self.dll.AUTDLinkAuditFpgaModulationFreqDivide.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaModulationFreqDivide.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaModulationCycle.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaModulationCycle.restype = ctypes.c_uint16

        self.dll.AUTDLinkAuditFpgaModulationBuffer.argtypes = [
            LinkPtr,
            ctypes.c_uint8,
            ctypes.c_uint16,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_uint32,
        ]
        self.dll.AUTDLinkAuditFpgaModulationBuffer.restype = None

        self.dll.AUTDLinkAuditFpgaModulationLoopBehavior.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16]
        self.dll.AUTDLinkAuditFpgaModulationLoopBehavior.restype = LoopBehavior

        self.dll.AUTDLinkAuditFpgaDrivesAt.argtypes = [LinkPtr, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint16, ctypes.POINTER(Drive)]
        self.dll.AUTDLinkAuditFpgaDrivesAt.restype = None

        self.dll.AUTDLinkAuditFpgaPulseWidthEncoderTable.argtypes = [LinkPtr, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint16)]
        self.dll.AUTDLinkAuditFpgaPulseWidthEncoderTable.restype = None

        self.dll.AUTDLinkGet.argtypes = [ControllerPtr]
        self.dll.AUTDLinkGet.restype = LinkPtr

        self.dll.AUTDLinkNop.argtypes = []
        self.dll.AUTDLinkNop.restype = LinkPtr

        self.dll.AUTDModulationCustom.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint16, SamplingConfigWrap]
        self.dll.AUTDModulationCustom.restype = ModulationPtr

        self.dll.AUTDModulationWithFir.argtypes = [ModulationPtr, ctypes.POINTER(ctypes.c_float), ctypes.c_uint32]
        self.dll.AUTDModulationWithFir.restype = ModulationPtr

        self.dll.AUTDModulationFourierExact.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(SineOption), ctypes.c_uint32, FourierOption]
        self.dll.AUTDModulationFourierExact.restype = ModulationPtr

        self.dll.AUTDModulationFourierExactFloat.argtypes = [
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(SineOption),
            ctypes.c_uint32,
            FourierOption,
        ]
        self.dll.AUTDModulationFourierExactFloat.restype = ModulationPtr

        self.dll.AUTDModulationFourierNearest.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(SineOption), ctypes.c_uint32, FourierOption]
        self.dll.AUTDModulationFourierNearest.restype = ModulationPtr

        self.dll.AUTDModulationSamplingConfig.argtypes = [ModulationPtr]
        self.dll.AUTDModulationSamplingConfig.restype = SamplingConfigWrap

        self.dll.AUTDModulationIntoDatagramWithSegment.argtypes = [ModulationPtr, ctypes.c_uint8, TransitionModeWrap]
        self.dll.AUTDModulationIntoDatagramWithSegment.restype = DatagramPtr

        self.dll.AUTDModulationIntoDatagramWithLoopBehavior.argtypes = [ModulationPtr, ctypes.c_uint8, TransitionModeWrap, LoopBehavior]
        self.dll.AUTDModulationIntoDatagramWithLoopBehavior.restype = DatagramPtr

        self.dll.AUTDModulationIntoDatagram.argtypes = [ModulationPtr]
        self.dll.AUTDModulationIntoDatagram.restype = DatagramPtr

        self.dll.AUTDModulationWithRadiationPressure.argtypes = [ModulationPtr]
        self.dll.AUTDModulationWithRadiationPressure.restype = ModulationPtr

        self.dll.AUTDModulationSineExact.argtypes = [ctypes.c_uint32, SineOption]
        self.dll.AUTDModulationSineExact.restype = ModulationPtr

        self.dll.AUTDModulationSineExactFloat.argtypes = [ctypes.c_float, SineOption]
        self.dll.AUTDModulationSineExactFloat.restype = ModulationPtr

        self.dll.AUTDModulationSineNearest.argtypes = [ctypes.c_float, SineOption]
        self.dll.AUTDModulationSineNearest.restype = ModulationPtr

        self.dll.AUTDModulationSineIsDefault.argtypes = [SineOption]
        self.dll.AUTDModulationSineIsDefault.restype = ctypes.c_bool

        self.dll.AUTDModulationSquareExact.argtypes = [ctypes.c_uint32, SquareOption]
        self.dll.AUTDModulationSquareExact.restype = ModulationPtr

        self.dll.AUTDModulationSquareExactFloat.argtypes = [ctypes.c_float, SquareOption]
        self.dll.AUTDModulationSquareExactFloat.restype = ModulationPtr

        self.dll.AUTDModulationSquareNearest.argtypes = [ctypes.c_float, SquareOption]
        self.dll.AUTDModulationSquareNearest.restype = ModulationPtr

        self.dll.AUTDModulationSquareIsDefault.argtypes = [SquareOption]
        self.dll.AUTDModulationSquareIsDefault.restype = ctypes.c_bool

        self.dll.AUTDModulationStatic.argtypes = [ctypes.c_uint8]
        self.dll.AUTDModulationStatic.restype = ModulationPtr

        self.dll.AUTDModulationStaticIsDefault.argtypes = [ctypes.c_uint8]
        self.dll.AUTDModulationStaticIsDefault.restype = ctypes.c_bool

        self.dll.AUTDGetErr.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.dll.AUTDGetErr.restype = None

    def controller_open(
        self,
        pos: ctypes.Array[Point3],
        rot: ctypes.Array[Quaternion],
        len_: int,
        link: LinkPtr,
        option: SenderOption,
        timer_strategy: TimerStrategyWrap,
    ) -> ResultController:
        return self.dll.AUTDControllerOpen(pos, rot, len_, link, option, timer_strategy)

    def controller_close(self, cnt: ControllerPtr) -> ResultStatus:
        return self.dll.AUTDControllerClose(cnt)

    def controller_fpga_state(self, cnt: ControllerPtr) -> ResultFPGAStateList:
        return self.dll.AUTDControllerFPGAState(cnt)

    def controller_fpga_state_get(self, p: FPGAStateListPtr, idx: int) -> ctypes.c_int16:
        return self.dll.AUTDControllerFPGAStateGet(p, idx)

    def controller_fpga_state_delete(self, p: FPGAStateListPtr) -> None:
        return self.dll.AUTDControllerFPGAStateDelete(p)

    def controller_firmware_version_list_pointer(self, cnt: ControllerPtr) -> ResultFirmwareVersionList:
        return self.dll.AUTDControllerFirmwareVersionListPointer(cnt)

    def controller_firmware_version_get(self, p_info_list: FirmwareVersionListPtr, idx: int, info: bytes) -> None:
        return self.dll.AUTDControllerFirmwareVersionGet(p_info_list, idx, info)

    def controller_firmware_version_list_pointer_delete(self, p_info_list: FirmwareVersionListPtr) -> None:
        return self.dll.AUTDControllerFirmwareVersionListPointerDelete(p_info_list)

    def firmware_latest(self, latest: bytes) -> None:
        return self.dll.AUTDFirmwareLatest(latest)

    def set_default_sender_option(self, cnt: ControllerPtr, option: SenderOption) -> None:
        return self.dll.AUTDSetDefaultSenderOption(cnt, option)

    def sender(self, cnt: ControllerPtr, option: SenderOption, timer_strategy: TimerStrategyWrap) -> SenderPtr:
        return self.dll.AUTDSender(cnt, option, timer_strategy)

    def sender_send(self, sender: SenderPtr, d: DatagramPtr) -> ResultStatus:
        return self.dll.AUTDSenderSend(sender, d)

    def spin_sleep_default_accuracy(self) -> ctypes.c_uint32:
        return self.dll.AUTDSpinSleepDefaultAccuracy()

    def sender_option_is_default(self, option: SenderOption) -> ctypes.c_bool:
        return self.dll.AUTDSenderOptionIsDefault(option)

    def datagram_clear(self) -> DatagramPtr:
        return self.dll.AUTDDatagramClear()

    def datagram_force_fan(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr) -> DatagramPtr:
        return self.dll.AUTDDatagramForceFan(f, context, geometry)

    def datagram_gpio_outputs(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr) -> DatagramPtr:
        return self.dll.AUTDDatagramGPIOOutputs(f, context, geometry)

    def datagram_group(
        self,
        f: ctypes.c_void_p,
        context: ctypes.c_void_p,
        geometry: GeometryPtr,
        keys: ctypes.Array[ctypes.c_int32],
        d: ctypes.Array[DatagramPtr],
        n: int,
    ) -> DatagramPtr:
        return self.dll.AUTDDatagramGroup(f, context, geometry, keys, d, n)

    def datagram_output_mask(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr) -> DatagramPtr:
        return self.dll.AUTDDatagramOutputMask(f, context, geometry)

    def datagram_output_mask_with_segment(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr, segment: Segment) -> DatagramPtr:
        return self.dll.AUTDDatagramOutputMaskWithSegment(f, context, geometry, segment)

    def datagram_phase_corr(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr) -> DatagramPtr:
        return self.dll.AUTDDatagramPhaseCorr(f, context, geometry)

    def datagram_pulse_width_encoder_256(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr) -> DatagramPtr:
        return self.dll.AUTDDatagramPulseWidthEncoder256(f, context, geometry)

    def datagram_pulse_width_encoder_256_default(self) -> DatagramPtr:
        return self.dll.AUTDDatagramPulseWidthEncoder256Default()

    def datagram_pulse_width_encoder_512(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr) -> DatagramPtr:
        return self.dll.AUTDDatagramPulseWidthEncoder512(f, context, geometry)

    def datagram_pulse_width_encoder_512_default(self) -> DatagramPtr:
        return self.dll.AUTDDatagramPulseWidthEncoder512Default()

    def datagram_reads_fpga_state(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr) -> DatagramPtr:
        return self.dll.AUTDDatagramReadsFPGAState(f, context, geometry)

    def datagram_swap_segment_modulation(self, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        return self.dll.AUTDDatagramSwapSegmentModulation(segment, transition_mode)

    def datagram_swap_segment_foci_stm(self, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        return self.dll.AUTDDatagramSwapSegmentFociSTM(segment, transition_mode)

    def datagram_swap_segment_gain_stm(self, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        return self.dll.AUTDDatagramSwapSegmentGainSTM(segment, transition_mode)

    def datagram_swap_segment_gain(self, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        return self.dll.AUTDDatagramSwapSegmentGain(segment, transition_mode)

    def datagram_silencer_from_update_rate(self, config: FixedUpdateRate) -> DatagramPtr:
        return self.dll.AUTDDatagramSilencerFromUpdateRate(config)

    def datagram_silencer_from_completion_steps(self, config: FixedCompletionSteps) -> DatagramPtr:
        return self.dll.AUTDDatagramSilencerFromCompletionSteps(config)

    def datagram_silencer_from_completion_time(self, config: FixedCompletionTime) -> DatagramPtr:
        return self.dll.AUTDDatagramSilencerFromCompletionTime(config)

    def datagram_silencer_fixed_completion_steps_is_default(self, config: FixedCompletionSteps) -> ctypes.c_bool:
        return self.dll.AUTDDatagramSilencerFixedCompletionStepsIsDefault(config)

    def stm_foci(self, config: SamplingConfigWrap, points: ctypes.c_void_p, size: int, n: int) -> FociSTMPtr:
        return self.dll.AUTDSTMFoci(config, points, size, n)

    def stm_foci_into_datagram_with_segment(self, stm: FociSTMPtr, n: int, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        return self.dll.AUTDSTMFociIntoDatagramWithSegment(stm, n, segment, transition_mode)

    def stm_foci_into_datagram_with_loop_behavior(
        self,
        stm: FociSTMPtr,
        n: int,
        segment: Segment,
        transition_mode: TransitionModeWrap,
        loop_behavior: LoopBehavior,
    ) -> DatagramPtr:
        return self.dll.AUTDSTMFociIntoDatagramWithLoopBehavior(stm, n, segment, transition_mode, loop_behavior)

    def stm_foci_into_datagram(self, stm: FociSTMPtr, n: int) -> DatagramPtr:
        return self.dll.AUTDSTMFociIntoDatagram(stm, n)

    def stm_gain(self, config: SamplingConfigWrap, gains: ctypes.Array[GainPtr], size: int, option: GainSTMOption) -> GainSTMPtr:
        return self.dll.AUTDSTMGain(config, gains, size, option)

    def stm_gain_into_datagram_with_segment(self, stm: GainSTMPtr, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        return self.dll.AUTDSTMGainIntoDatagramWithSegment(stm, segment, transition_mode)

    def stm_gain_into_datagram_with_loop_behavior(
        self,
        stm: GainSTMPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap,
        loop_behavior: LoopBehavior,
    ) -> DatagramPtr:
        return self.dll.AUTDSTMGainIntoDatagramWithLoopBehavior(stm, segment, transition_mode, loop_behavior)

    def stm_gain_into_datagram(self, stm: GainSTMPtr) -> DatagramPtr:
        return self.dll.AUTDSTMGainIntoDatagram(stm)

    def stm_config_from_freq(self, f: float, n: int) -> ResultSamplingConfig:
        return self.dll.AUTDSTMConfigFromFreq(f, n)

    def stm_config_from_period(self, p: Duration, n: int) -> ResultSamplingConfig:
        return self.dll.AUTDSTMConfigFromPeriod(p, n)

    def stm_config_from_freq_nearest(self, f: float, n: int) -> SamplingConfigWrap:
        return self.dll.AUTDSTMConfigFromFreqNearest(f, n)

    def stm_config_from_period_nearest(self, p: Duration, n: int) -> SamplingConfigWrap:
        return self.dll.AUTDSTMConfigFromPeriodNearest(p, n)

    def datagram_synchronize(self) -> DatagramPtr:
        return self.dll.AUTDDatagramSynchronize()

    def datagram_tuple(self, d1: DatagramPtr, d2: DatagramPtr) -> DatagramPtr:
        return self.dll.AUTDDatagramTuple(d1, d2)

    def dc_sys_time_now(self) -> DcSysTime:
        return self.dll.AUTDDcSysTimeNow()

    def gpio_output_type_none(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeNone()

    def gpio_output_type_base_signal(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeBaseSignal()

    def gpio_output_type_thermo(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeThermo()

    def gpio_output_type_force_fan(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeForceFan()

    def gpio_output_type_sync(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeSync()

    def gpio_output_type_mod_segment(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeModSegment()

    def gpio_output_type_mod_idx(self, value: int) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeModIdx(value)

    def gpio_output_type_stm_segment(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeStmSegment()

    def gpio_output_type_stm_idx(self, value: int) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeStmIdx(value)

    def gpio_output_type_is_stm_mode(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeIsStmMode()

    def gpio_output_type_pwm_out(self, value: TransducerPtr) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypePwmOut(value)

    def gpio_output_type_direct(self, value: bool) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeDirect(value)

    def gpio_output_type_sys_time_eq(self, sys_time: DcSysTime) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeSysTimeEq(sys_time)

    def gpio_output_type_sync_diff(self) -> GPIOOutputTypeWrap:
        return self.dll.AUTDGPIOOutputTypeSyncDiff()

    def loop_behavior_infinite(self) -> LoopBehavior:
        return self.dll.AUTDLoopBehaviorInfinite()

    def loop_behavior_finite(self, v: int) -> LoopBehavior:
        return self.dll.AUTDLoopBehaviorFinite(v)

    def phase_from_rad(self, value: float) -> ctypes.c_uint8:
        return self.dll.AUTDPhaseFromRad(value)

    def phase_to_rad(self, value: Phase) -> ctypes.c_float:
        return self.dll.AUTDPhaseToRad(value)

    def pulse_width_256(self, value: int) -> ResultU8:
        return self.dll.AUTDPulseWidth256(value)

    def pulse_width_512(self, value: int) -> ResultU16:
        return self.dll.AUTDPulseWidth512(value)

    def pulse_width_256_from_duty(self, duty: float) -> ResultU8:
        return self.dll.AUTDPulseWidth256FromDuty(duty)

    def pulse_width_512_from_duty(self, duty: float) -> ResultU16:
        return self.dll.AUTDPulseWidth512FromDuty(duty)

    def sampling_config_from_divide(self, div: int) -> ResultSamplingConfig:
        return self.dll.AUTDSamplingConfigFromDivide(div)

    def sampling_config_from_freq(self, f: float) -> SamplingConfigWrap:
        return self.dll.AUTDSamplingConfigFromFreq(f)

    def sampling_config_from_period(self, p: Duration) -> SamplingConfigWrap:
        return self.dll.AUTDSamplingConfigFromPeriod(p)

    def sampling_config_into_nearest(self, config: SamplingConfigWrap) -> SamplingConfigWrap:
        return self.dll.AUTDSamplingConfigIntoNearest(config)

    def sampling_config_divide(self, c: SamplingConfigWrap) -> ResultU16:
        return self.dll.AUTDSamplingConfigDivide(c)

    def sampling_config_freq(self, c: SamplingConfigWrap) -> ResultF32:
        return self.dll.AUTDSamplingConfigFreq(c)

    def sampling_config_period(self, c: SamplingConfigWrap) -> ResultDuration:
        return self.dll.AUTDSamplingConfigPeriod(c)

    def sampling_config_eq(self, a: SamplingConfigWrap, b: SamplingConfigWrap) -> ctypes.c_bool:
        return self.dll.AUTDSamplingConfigEq(a, b)

    def transition_mode_sync_idx(self) -> TransitionModeWrap:
        return self.dll.AUTDTransitionModeSyncIdx()

    def transition_mode_sys_time(self, sys_time: DcSysTime) -> TransitionModeWrap:
        return self.dll.AUTDTransitionModeSysTime(sys_time)

    def transition_mode_gpio(self, gpio: GPIOIn) -> TransitionModeWrap:
        return self.dll.AUTDTransitionModeGPIO(gpio)

    def transition_mode_ext(self) -> TransitionModeWrap:
        return self.dll.AUTDTransitionModeExt()

    def transition_mode_immediate(self) -> TransitionModeWrap:
        return self.dll.AUTDTransitionModeImmediate()

    def transition_mode_none(self) -> TransitionModeWrap:
        return self.dll.AUTDTransitionModeNone()

    def environment(self, cnt: ControllerPtr) -> EnvironmentPtr:
        return self.dll.AUTDEnvironment(cnt)

    def environment_get_sound_speed(self, env: EnvironmentPtr) -> ctypes.c_float:
        return self.dll.AUTDEnvironmentGetSoundSpeed(env)

    def environment_set_sound_speed(self, env: EnvironmentPtr, value: float) -> None:
        return self.dll.AUTDEnvironmentSetSoundSpeed(env, value)

    def environment_set_sound_speed_from_temp(self, env: EnvironmentPtr, temp: float, k: float, r: float, m: float) -> None:
        return self.dll.AUTDEnvironmentSetSoundSpeedFromTemp(env, temp, k, r, m)

    def environment_wavelength(self, env: EnvironmentPtr) -> ctypes.c_float:
        return self.dll.AUTDEnvironmentWavelength(env)

    def environment_wavenumber(self, env: EnvironmentPtr) -> ctypes.c_float:
        return self.dll.AUTDEnvironmentWavenumber(env)

    def gain_bessel(self, pos: Point3, dir_: Vector3, theta: Angle, option: BesselOption) -> GainPtr:
        return self.dll.AUTDGainBessel(pos, dir_, theta, option)

    def gain_bessel_is_default(self, option: BesselOption) -> ctypes.c_bool:
        return self.dll.AUTDGainBesselIsDefault(option)

    def gain_custom(self, f: ctypes.c_void_p, context: ctypes.c_void_p, geometry: GeometryPtr) -> GainPtr:
        return self.dll.AUTDGainCustom(f, context, geometry)

    def gain_focus(self, pos: Point3, option: FocusOption) -> GainPtr:
        return self.dll.AUTDGainFocus(pos, option)

    def gain_focus_is_default(self, option: FocusOption) -> ctypes.c_bool:
        return self.dll.AUTDGainFocusIsDefault(option)

    def gain_group_create_map(self, device_indices_ptr: ctypes.Array[ctypes.c_uint16], num_devices: int) -> GroupGainMapPtr:
        return self.dll.AUTDGainGroupCreateMap(device_indices_ptr, num_devices)

    def gain_group_map_set(self, map_: GroupGainMapPtr, dev_idx: int, map_data: ctypes.Array[ctypes.c_int32]) -> GroupGainMapPtr:
        return self.dll.AUTDGainGroupMapSet(map_, dev_idx, map_data)

    def gain_group(self, map_: GroupGainMapPtr, keys_ptr: ctypes.Array[ctypes.c_int32], values_ptr: ctypes.Array[GainPtr], kv_len: int) -> GainPtr:
        return self.dll.AUTDGainGroup(map_, keys_ptr, values_ptr, kv_len)

    def gain_into_datagram_with_segment(self, gain: GainPtr, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        return self.dll.AUTDGainIntoDatagramWithSegment(gain, segment, transition_mode)

    def gain_into_datagram(self, gain: GainPtr) -> DatagramPtr:
        return self.dll.AUTDGainIntoDatagram(gain)

    def gain_null(self) -> GainPtr:
        return self.dll.AUTDGainNull()

    def gain_plane(self, n: Vector3, option: PlaneOption) -> GainPtr:
        return self.dll.AUTDGainPlane(n, option)

    def gain_planel_is_default(self, option: PlaneOption) -> ctypes.c_bool:
        return self.dll.AUTDGainPlanelIsDefault(option)

    def gain_uniform(self, intensity: Intensity, phase: Phase) -> GainPtr:
        return self.dll.AUTDGainUniform(intensity, phase)

    def device(self, geo: GeometryPtr, dev_idx: int) -> DevicePtr:
        return self.dll.AUTDDevice(geo, dev_idx)

    def device_num_transducers(self, dev: DevicePtr) -> ctypes.c_uint32:
        return self.dll.AUTDDeviceNumTransducers(dev)

    def device_center(self, dev: DevicePtr) -> Point3:
        return self.dll.AUTDDeviceCenter(dev)

    def device_rotation(self, dev: DevicePtr) -> Quaternion:
        return self.dll.AUTDDeviceRotation(dev)

    def device_direction_x(self, dev: DevicePtr) -> Vector3:
        return self.dll.AUTDDeviceDirectionX(dev)

    def device_direction_y(self, dev: DevicePtr) -> Vector3:
        return self.dll.AUTDDeviceDirectionY(dev)

    def device_direction_axial(self, dev: DevicePtr) -> Vector3:
        return self.dll.AUTDDeviceDirectionAxial(dev)

    def geometry(self, cnt: ControllerPtr) -> GeometryPtr:
        return self.dll.AUTDGeometry(cnt)

    def geometry_num_devices(self, geo: GeometryPtr) -> ctypes.c_uint32:
        return self.dll.AUTDGeometryNumDevices(geo)

    def geometry_num_transducers(self, geo: GeometryPtr) -> ctypes.c_uint32:
        return self.dll.AUTDGeometryNumTransducers(geo)

    def geometr_center(self, geo: GeometryPtr) -> Point3:
        return self.dll.AUTDGeometrCenter(geo)

    def geometry_reconfigure(self, geo: GeometryPtr, pos: ctypes.Array[Point3], rot: ctypes.Array[Quaternion]) -> None:
        return self.dll.AUTDGeometryReconfigure(geo, pos, rot)

    def rotation_from_euler_xyz(self, x: float, y: float, z: float) -> Quaternion:
        return self.dll.AUTDRotationFromEulerXYZ(x, y, z)

    def rotation_from_euler_zyz(self, z1: float, y: float, z2: float) -> Quaternion:
        return self.dll.AUTDRotationFromEulerZYZ(z1, y, z2)

    def transducer(self, dev: DevicePtr, idx: int) -> TransducerPtr:
        return self.dll.AUTDTransducer(dev, idx)

    def transducer_position(self, tr: TransducerPtr) -> Point3:
        return self.dll.AUTDTransducerPosition(tr)

    def link_audit(self) -> LinkPtr:
        return self.dll.AUTDLinkAudit()

    def link_audit_is_open(self, audit: LinkPtr) -> ctypes.c_bool:
        return self.dll.AUTDLinkAuditIsOpen(audit)

    def link_audit_break_down(self, audit: LinkPtr) -> None:
        return self.dll.AUTDLinkAuditBreakDown(audit)

    def link_audit_repair(self, audit: LinkPtr) -> None:
        return self.dll.AUTDLinkAuditRepair(audit)

    def link_audit_cpu_num_transducers(self, audit: LinkPtr, idx: int) -> ctypes.c_uint32:
        return self.dll.AUTDLinkAuditCpuNumTransducers(audit, idx)

    def link_audit_fpga_assert_thermal_sensor(self, audit: LinkPtr, idx: int) -> None:
        return self.dll.AUTDLinkAuditFpgaAssertThermalSensor(audit, idx)

    def link_audit_fpga_deassert_thermal_sensor(self, audit: LinkPtr, idx: int) -> None:
        return self.dll.AUTDLinkAuditFpgaDeassertThermalSensor(audit, idx)

    def link_audit_fpga_is_force_fan(self, audit: LinkPtr, idx: int) -> ctypes.c_bool:
        return self.dll.AUTDLinkAuditFpgaIsForceFan(audit, idx)

    def link_audit_fpga_current_stm_segment(self, audit: LinkPtr, idx: int) -> Segment:
        return self.dll.AUTDLinkAuditFpgaCurrentStmSegment(audit, idx)

    def link_audit_fpga_current_mod_segment(self, audit: LinkPtr, idx: int) -> Segment:
        return self.dll.AUTDLinkAuditFpgaCurrentModSegment(audit, idx)

    def link_audit_fpga_is_stm_gain_mode(self, audit: LinkPtr, segment: Segment, idx: int) -> ctypes.c_bool:
        return self.dll.AUTDLinkAuditFpgaIsStmGainMode(audit, segment, idx)

    def link_audit_cpu_silencer_strict(self, audit: LinkPtr, idx: int) -> ctypes.c_bool:
        return self.dll.AUTDLinkAuditCpuSilencerStrict(audit, idx)

    def link_audit_fpga_silencer_update_rate_intensity(self, audit: LinkPtr, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaSilencerUpdateRateIntensity(audit, idx)

    def link_audit_fpga_silencer_update_rate_phase(self, audit: LinkPtr, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaSilencerUpdateRatePhase(audit, idx)

    def link_audit_fpga_silencer_completion_steps_intensity(self, audit: LinkPtr, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaSilencerCompletionStepsIntensity(audit, idx)

    def link_audit_fpga_silencer_completion_steps_phase(self, audit: LinkPtr, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaSilencerCompletionStepsPhase(audit, idx)

    def link_audit_fpga_silencer_fixed_completion_steps_mode(self, audit: LinkPtr, idx: int) -> ctypes.c_bool:
        return self.dll.AUTDLinkAuditFpgaSilencerFixedCompletionStepsMode(audit, idx)

    def link_audit_fpga_gpio_output_types(self, audit: LinkPtr, idx: int, ty: ctypes.Array[ctypes.c_uint8]) -> None:
        return self.dll.AUTDLinkAuditFpgaGPIOOutputTypes(audit, idx, ty)

    def link_audit_fpga_debug_values(self, audit: LinkPtr, idx: int, value: ctypes.Array[ctypes.c_uint64]) -> None:
        return self.dll.AUTDLinkAuditFpgaDebugValues(audit, idx, value)

    def link_audit_fpga_stm_freq_divide(self, audit: LinkPtr, segment: Segment, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaStmFreqDivide(audit, segment, idx)

    def link_audit_fpga_stm_cycle(self, audit: LinkPtr, segment: Segment, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaStmCycle(audit, segment, idx)

    def link_audit_fpga_sound_speed(self, audit: LinkPtr, segment: Segment, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaSoundSpeed(audit, segment, idx)

    def link_audit_fpga_stm_loop_behavior(self, audit: LinkPtr, segment: Segment, idx: int) -> LoopBehavior:
        return self.dll.AUTDLinkAuditFpgaStmLoopBehavior(audit, segment, idx)

    def link_audit_fpga_modulation_freq_divide(self, audit: LinkPtr, segment: Segment, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaModulationFreqDivide(audit, segment, idx)

    def link_audit_fpga_modulation_cycle(self, audit: LinkPtr, segment: Segment, idx: int) -> ctypes.c_uint16:
        return self.dll.AUTDLinkAuditFpgaModulationCycle(audit, segment, idx)

    def link_audit_fpga_modulation_buffer(self, audit: LinkPtr, segment: Segment, idx: int, data: ctypes.Array[ctypes.c_uint8], size: int) -> None:
        return self.dll.AUTDLinkAuditFpgaModulationBuffer(audit, segment, idx, data, size)

    def link_audit_fpga_modulation_loop_behavior(self, audit: LinkPtr, segment: Segment, idx: int) -> LoopBehavior:
        return self.dll.AUTDLinkAuditFpgaModulationLoopBehavior(audit, segment, idx)

    def link_audit_fpga_drives_at(self, audit: LinkPtr, segment: Segment, idx: int, stm_idx: int, drive: ctypes.Array[Drive]) -> None:
        return self.dll.AUTDLinkAuditFpgaDrivesAt(audit, segment, idx, stm_idx, drive)

    def link_audit_fpga_pulse_width_encoder_table(self, audit: LinkPtr, idx: int, dst: ctypes.Array[ctypes.c_uint16]) -> None:
        return self.dll.AUTDLinkAuditFpgaPulseWidthEncoderTable(audit, idx, dst)

    def link_get(self, cnt: ControllerPtr) -> LinkPtr:
        return self.dll.AUTDLinkGet(cnt)

    def link_nop(self) -> LinkPtr:
        return self.dll.AUTDLinkNop()

    def modulation_custom(self, ptr: ctypes.Array[ctypes.c_uint8], len_: int, sampling_config: SamplingConfigWrap) -> ModulationPtr:
        return self.dll.AUTDModulationCustom(ptr, len_, sampling_config)

    def modulation_with_fir(self, m: ModulationPtr, coef: ctypes.Array[ctypes.c_float], n_tap: int) -> ModulationPtr:
        return self.dll.AUTDModulationWithFir(m, coef, n_tap)

    def modulation_fourier_exact(
        self,
        sine_freq: ctypes.Array[ctypes.c_uint32],
        sine_option: ctypes.Array[SineOption],
        size: int,
        option: FourierOption,
    ) -> ModulationPtr:
        return self.dll.AUTDModulationFourierExact(sine_freq, sine_option, size, option)

    def modulation_fourier_exact_float(
        self,
        sine_freq: ctypes.Array[ctypes.c_float],
        sine_option: ctypes.Array[SineOption],
        size: int,
        option: FourierOption,
    ) -> ModulationPtr:
        return self.dll.AUTDModulationFourierExactFloat(sine_freq, sine_option, size, option)

    def modulation_fourier_nearest(
        self,
        sine_freq: ctypes.Array[ctypes.c_float],
        sine_option: ctypes.Array[SineOption],
        size: int,
        option: FourierOption,
    ) -> ModulationPtr:
        return self.dll.AUTDModulationFourierNearest(sine_freq, sine_option, size, option)

    def modulation_sampling_config(self, m: ModulationPtr) -> SamplingConfigWrap:
        return self.dll.AUTDModulationSamplingConfig(m)

    def modulation_into_datagram_with_segment(self, m: ModulationPtr, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        return self.dll.AUTDModulationIntoDatagramWithSegment(m, segment, transition_mode)

    def modulation_into_datagram_with_loop_behavior(
        self,
        m: ModulationPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap,
        loop_behavior: LoopBehavior,
    ) -> DatagramPtr:
        return self.dll.AUTDModulationIntoDatagramWithLoopBehavior(m, segment, transition_mode, loop_behavior)

    def modulation_into_datagram(self, m: ModulationPtr) -> DatagramPtr:
        return self.dll.AUTDModulationIntoDatagram(m)

    def modulation_with_radiation_pressure(self, m: ModulationPtr) -> ModulationPtr:
        return self.dll.AUTDModulationWithRadiationPressure(m)

    def modulation_sine_exact(self, freq: int, option: SineOption) -> ModulationPtr:
        return self.dll.AUTDModulationSineExact(freq, option)

    def modulation_sine_exact_float(self, freq: float, option: SineOption) -> ModulationPtr:
        return self.dll.AUTDModulationSineExactFloat(freq, option)

    def modulation_sine_nearest(self, freq: float, option: SineOption) -> ModulationPtr:
        return self.dll.AUTDModulationSineNearest(freq, option)

    def modulation_sine_is_default(self, option: SineOption) -> ctypes.c_bool:
        return self.dll.AUTDModulationSineIsDefault(option)

    def modulation_square_exact(self, freq: int, option: SquareOption) -> ModulationPtr:
        return self.dll.AUTDModulationSquareExact(freq, option)

    def modulation_square_exact_float(self, freq: float, option: SquareOption) -> ModulationPtr:
        return self.dll.AUTDModulationSquareExactFloat(freq, option)

    def modulation_square_nearest(self, freq: float, option: SquareOption) -> ModulationPtr:
        return self.dll.AUTDModulationSquareNearest(freq, option)

    def modulation_square_is_default(self, option: SquareOption) -> ctypes.c_bool:
        return self.dll.AUTDModulationSquareIsDefault(option)

    def modulation_static(self, intensity: int) -> ModulationPtr:
        return self.dll.AUTDModulationStatic(intensity)

    def modulation_static_is_default(self, intensity: int) -> ctypes.c_bool:
        return self.dll.AUTDModulationStaticIsDefault(intensity)

    def get_err(self, src: ctypes.c_void_p, dst: bytes) -> None:
        return self.dll.AUTDGetErr(src, dst)
