import contextlib

from .controller import Controller
from .driver.autd3_device import AUTD3
from .driver.datagram import (
    Clear,
    DebugSettings,
    DebugType,
    FixedCompletionTime,
    FixedUpdateRate,
    FociSTM,
    ForceFan,
    GainSTM,
    GainSTMMode,
    PhaseCorrection,
    PulseWidthEncoder,
    ReadsFPGAState,
    Silencer,
    SwapSegment,
)
from .driver.datagram.stm import (
    ControlPoint,
    ControlPoints1,
    ControlPoints2,
    ControlPoints3,
    ControlPoints4,
    ControlPoints5,
    ControlPoints6,
    ControlPoints7,
    ControlPoints8,
)
from .driver.defined import Hz, deg, kHz, rad
from .driver.firmware.fpga import Drive, EmitIntensity, LoopBehavior, Phase, SamplingConfig, TransitionMode
from .driver.geometry import Device, EulerAngles, Geometry, Transducer
from .ethercat import DcSysTime
from .gain import Bessel, Focus, Group, Null, Plane, Uniform
from .link.nop import Nop
from .modulation import Sine, Square, Static
from .native_methods.autd3capi import NativeMethods as Base
from .native_methods.autd3capi_driver import (
    GPIOIn,
    GPIOOut,
    Segment,
    SilencerTarget,
)
from .native_methods.autd3capi_emulator import NativeMethods as Emulator
from .native_methods.autd3capi_link_simulator import NativeMethods as Simulator
from .native_methods.autd3capi_link_twincat import NativeMethods as TwinCAT
from .native_methods.autd3capi_modulation_audio_file import NativeMethods as AudioFile


def tracing_init() -> None:
    Base().tracing_init()
    with contextlib.suppress(BaseException):
        Emulator().emulator_tracing_init()
    with contextlib.suppress(BaseException):
        Simulator().link_simulator_tracing_init()
    with contextlib.suppress(BaseException):
        TwinCAT().link_twin_cat_tracing_init()
    with contextlib.suppress(BaseException):
        AudioFile().modulation_audio_file_tracing_init()


__all__ = [
    "tracing_init",
    "Controller",
    "AUTD3",
    "PhaseCorrection",
    "Drive",
    "EmitIntensity",
    "Phase",
    "phase_rad",
    "SamplingConfig",
    "Clear",
    "Silencer",
    "FixedCompletionTime",
    "FixedUpdateRate",
    "DebugSettings",
    "DebugType",
    "ReadsFPGAState",
    "ForceFan",
    "ControlPoint",
    "ControlPoints1",
    "ControlPoints2",
    "ControlPoints3",
    "ControlPoints4",
    "ControlPoints5",
    "ControlPoints6",
    "ControlPoints7",
    "ControlPoints8",
    "FociSTM",
    "GainSTM",
    "GainSTMMode",
    "Device",
    "EulerAngles",
    "Geometry",
    "Transducer",
    "deg",
    "rad",
    "Bessel",
    "Focus",
    "Group",
    "Null",
    "Plane",
    "Custom",
    "Uniform",
    "Nop",
    "SamplingMode",
    "Sine",
    "Square",
    "Static",
    "LoopBehavior",
    "Segment",
    "SwapSegment",
    "GPIOIn",
    "GPIOOut",
    "Hz",
    "kHz",
    "DcSysTime",
    "PulseWidthEncoder",
    "TransitionMode",
    "SilencerTarget",
]

__version__ = "29.0.0rc5"
