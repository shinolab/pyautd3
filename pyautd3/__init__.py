import contextlib
from collections.abc import Callable

from .controller import Controller, SenderOption
from .controller.sleeper import SpinSleeper
from .driver.autd3_device import AUTD3
from .driver.datagram import (
    Clear,
    FixedCompletionTime,
    FixedUpdateRate,
    FociSTM,
    ForceFan,
    GainSTM,
    GainSTMOption,
    GPIOOutputs,
    GPIOOutputType,
    PhaseCorrection,
    PulseWidthEncoder,
    ReadsFPGAState,
    Silencer,
    SwapSegment,
    WithLoopBehavior,
    WithSegment,
)
from .driver.datagram.stm import ControlPoint, ControlPoints
from .driver.defined import Hz, deg, kHz, rad
from .driver.firmware.fpga import Drive, EmitIntensity, LoopBehavior, Phase, PulseWidth, SamplingConfig, TransitionMode
from .driver.geometry import Device, EulerAngles, Geometry, Transducer
from .ethercat import DcSysTime
from .gain import Bessel, BesselOption, Focus, FocusOption, Group, Null, Plane, PlaneOption, Uniform
from .link.nop import Nop
from .modulation import Sine, SineOption, Square, SquareOption, Static
from .native_methods.autd3 import GainSTMMode, GPIOIn, GPIOOut, ParallelMode, Segment
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
    "ControlPoints",
    "Controller",
    "Custom",
    "DcSysTime",
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
    "GPIOOutputType",
    "GPIOOutputs",
    "GainSTM",
    "GainSTMMode",
    "GainSTMOption",
    "Geometry",
    "Group",
    "Hz",
    "LoopBehavior",
    "Nop",
    "Null",
    "ParallelMode",
    "Phase",
    "PhaseCorrection",
    "Plane",
    "PlaneOption",
    "PulseWidth",
    "PulseWidthEncoder",
    "ReadsFPGAState",
    "SamplingConfig",
    "SamplingMode",
    "Segment",
    "SenderOption",
    "Silencer",
    "Sine",
    "SineOption",
    "SpinSleeper",
    "Square",
    "SquareOption",
    "Static",
    "SwapSegment",
    "Transducer",
    "TransitionMode",
    "Uniform",
    "WithLoopBehavior",
    "WithSegment",
    "deg",
    "kHz",
    "phase_rad",
    "rad",
    "tracing_init",
]

__version__ = "32.0.0"
