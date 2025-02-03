import contextlib
from collections.abc import Callable

from .controller import Controller, SenderOption
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
    GainSTMOption,
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
from .gain import Bessel, BesselOption, Focus, FocusOption, Group, Null, Plane, PlaneOption, Uniform
from .link.nop import Nop
from .modulation import Sine, SineOption, Square, SquareOption, Static
from .native_methods.autd3 import GainSTMMode, GPIOIn, GPIOOut, Segment, SilencerTarget
from .native_methods.autd3capi import NativeMethods as Base
from .native_methods.autd3capi_link_simulator import NativeMethods as Simulator
from .native_methods.autd3capi_link_twincat import NativeMethods as TwinCAT
from .native_methods.autd3capi_modulation_audio_file import NativeMethods as AudioFile
from .utils import Duration

_ext_tracing_init: list[Callable[[], None]] = []


def tracing_init() -> None:
    Base().tracing_init()
    with contextlib.suppress(BaseException):
        Simulator().link_simulator_tracing_init()
    with contextlib.suppress(BaseException):
        TwinCAT().link_twin_cat_tracing_init()
    with contextlib.suppress(BaseException):
        AudioFile().modulation_audio_file_tracing_init()
    for func in _ext_tracing_init:  # pragma: no cover
        func()  # pragma: no cover


__all__ = [
    "AUTD3",
    "Bessel",
    "BesselOption",
    "Clear",
    "ControlPoint",
    "ControlPoints1",
    "ControlPoints2",
    "ControlPoints3",
    "ControlPoints4",
    "ControlPoints5",
    "ControlPoints6",
    "ControlPoints7",
    "ControlPoints8",
    "Controller",
    "Custom",
    "DcSysTime",
    "DebugSettings",
    "DebugType",
    "Device",
    "Drive",
    "Duration",
    "EmitIntensity",
    "EulerAngles",
    "FixedCompletionTime",
    "FixedUpdateRate",
    "FociSTM",
    "Focus",
    "FocusOption",
    "ForceFan",
    "GPIOIn",
    "GPIOOut",
    "GainSTM",
    "GainSTMMode",
    "GainSTMOption",
    "Geometry",
    "Group",
    "Hz",
    "LoopBehavior",
    "Nop",
    "Null",
    "Phase",
    "PhaseCorrection",
    "Plane",
    "PlaneOption",
    "PulseWidthEncoder",
    "ReadsFPGAState",
    "SamplingConfig",
    "SamplingMode",
    "Segment",
    "SenderOption",
    "Silencer",
    "SilencerTarget",
    "Sine",
    "SineOption",
    "Square",
    "SquareOption",
    "Static",
    "SwapSegment",
    "Transducer",
    "TransitionMode",
    "Uniform",
    "deg",
    "kHz",
    "phase_rad",
    "rad",
    "tracing_init",
]

__version__ = "29.0.0rc19"
