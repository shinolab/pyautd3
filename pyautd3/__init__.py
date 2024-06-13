from enum import Enum

from .controller import Controller
from .driver.autd3_device import AUTD3
from .driver.datagram import (
    Clear,
    DebugSettings,
    DebugType,
    FociSTM,
    ForceFan,
    GainSTM,
    GainSTMMode,
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
from .native_methods.autd3capi import TRACE_LEVEL_DEBUG, TRACE_LEVEL_ERROR, TRACE_LEVEL_INFO, TRACE_LEVEL_TRACE, TRACE_LEVEL_WARN
from .native_methods.autd3capi import NativeMethods as Base
from .native_methods.autd3capi_driver import GPIOIn, GPIOOut, Segment


class Level(Enum):
    DEBUG = TRACE_LEVEL_DEBUG
    INFO = TRACE_LEVEL_INFO
    WARN = TRACE_LEVEL_WARN
    ERROR = TRACE_LEVEL_ERROR
    TRACE = TRACE_LEVEL_TRACE


def tracing_init(level: Level) -> None:
    Base().tracing_init(level.value)


__all__ = [
    "tracing_init",
    "Controller",
    "AUTD3",
    "Drive",
    "EmitIntensity",
    "Phase",
    "phase_rad",
    "SamplingConfig",
    "Clear",
    "Silencer",
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
]

__version__ = "25.2.1"
