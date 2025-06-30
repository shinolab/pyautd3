from collections.abc import Callable

from .controller import Controller, FixedSchedule, SenderOption
from .controller.sleeper import SpinSleeper
from .driver.autd3_device import AUTD3
from .driver.common import Hz, deg, kHz, rad
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
    Group,
    OutputMask,
    PhaseCorrection,
    PulseWidthEncoder,
    ReadsFPGAState,
    Silencer,
    SwapSegment,
    WithLoopBehavior,
    WithSegment,
)
from .driver.datagram.stm import ControlPoint, ControlPoints
from .driver.firmware.fpga import Drive, Intensity, LoopBehavior, Phase, PulseWidth, SamplingConfig, TransitionMode
from .driver.geometry import Device, EulerAngles, Geometry, Transducer
from .ethercat import DcSysTime
from .gain import Bessel, BesselOption, Focus, FocusOption, GainGroup, Null, Plane, PlaneOption, Uniform
from .link.nop import Nop
from .modulation import Sine, SineOption, Square, SquareOption, Static
from .native_methods.autd3 import GainSTMMode, GPIOIn, GPIOOut, ParallelMode, Segment
from .utils import Duration

_ext_tracing_init: list[Callable[[], None]] = []


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
    "EulerAngles",
    "FixedCompletionTime",
    "FixedSchedule",
    "FixedUpdateRate",
    "FociSTM",
    "Focus",
    "FocusOption",
    "ForceFan",
    "GPIOIn",
    "GPIOOut",
    "GPIOOutputType",
    "GPIOOutputs",
    "GainGroup",
    "GainSTM",
    "GainSTMMode",
    "GainSTMOption",
    "Geometry",
    "Group",
    "Hz",
    "Intensity",
    "LoopBehavior",
    "Nop",
    "Null",
    "OutputMask",
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

__version__ = "35.0.0"
