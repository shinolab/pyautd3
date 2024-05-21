from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import (
    Controller,
    DebugSettings,
    DebugType,
)
from pyautd3.driver.geometry.device import Device
from pyautd3.native_methods.autd3capi_driver import DebugTypeWrap, GPIOOut
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_debug_output_idx():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert np.array_equal([0x00, 0x00, 0x00, 0x00], autd.link.debug_types(dev.idx))
            assert np.array_equal([0x0000, 0x0000, 0x0000, 0x0000], autd.link.debug_values(dev.idx))

        def f0(_: Device, gpio: GPIOOut) -> DebugTypeWrap:
            match gpio:
                case GPIOOut.O0:
                    return DebugType.NONE
                case GPIOOut.O1:
                    return DebugType.BaseSignal
                case GPIOOut.O2:
                    return DebugType.Thermo
                case GPIOOut.O3:
                    return DebugType.ForceFan

        autd.send(DebugSettings(f0))
        for dev in autd.geometry:
            assert np.array_equal([0x00, 0x01, 0x02, 0x03], autd.link.debug_types(dev.idx))
            assert np.array_equal([0x0000, 0x0000, 0x0000, 0x0000], autd.link.debug_values(dev.idx))

        def f1(_: Device, gpio: GPIOOut) -> DebugTypeWrap:
            match gpio:
                case GPIOOut.O0:
                    return DebugType.Sync
                case GPIOOut.O1:
                    return DebugType.ModSegment
                case GPIOOut.O2:
                    return DebugType.ModIdx(0x01)
                case GPIOOut.O3:
                    return DebugType.StmSegment

        autd.send(DebugSettings(f1))
        for dev in autd.geometry:
            assert np.array_equal([0x10, 0x20, 0x21, 0x50], autd.link.debug_types(dev.idx))
            assert np.array_equal([0x0000, 0x0000, 0x0001, 0x0000], autd.link.debug_values(dev.idx))

        def f2(dev: Device, gpio: GPIOOut) -> DebugTypeWrap:
            match gpio:
                case GPIOOut.O0:
                    return DebugType.StmIdx(0x02)
                case GPIOOut.O1:
                    return DebugType.IsStmMode
                case GPIOOut.O2:
                    return DebugType.PwmOut(dev[3])
                case GPIOOut.O3:
                    return DebugType.Direct(True)  # noqa: FBT003

        autd.send(DebugSettings(f2))
        for dev in autd.geometry:
            assert np.array_equal([0x51, 0x52, 0xE0, 0xF0], autd.link.debug_types(dev.idx))
            assert np.array_equal([0x0002, 0x0000, 0x0003, 0x0001], autd.link.debug_values(dev.idx))
