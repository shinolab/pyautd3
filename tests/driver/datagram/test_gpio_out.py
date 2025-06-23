from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import (
    Controller,
    DcSysTime,
    GPIOOutputs,
    GPIOOutputType,
)
from pyautd3.driver.geometry.device import Device
from pyautd3.native_methods.autd3 import GPIOOut
from pyautd3.native_methods.autd3capi_driver import GPIOOutputTypeWrap
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_debug_output_idx():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert np.array_equal([0x00, 0x00, 0x00, 0x00], autd.link().debug_types(dev.idx()))
            assert np.array_equal([0x0000, 0x0000, 0x0000, 0x0000], autd.link().debug_values(dev.idx()))

        def f0(_: Device, gpio: GPIOOut) -> GPIOOutputTypeWrap | None:
            match gpio:
                case GPIOOut.O0:
                    return None
                case GPIOOut.O1:
                    return GPIOOutputType.BaseSignal
                case GPIOOut.O2:
                    return GPIOOutputType.Thermo
                case GPIOOut.O3:
                    return GPIOOutputType.ForceFan

        autd.send(GPIOOutputs(f0))
        for dev in autd.geometry():
            assert np.array_equal([0x00, 0x01, 0x02, 0x03], autd.link().debug_types(dev.idx()))
            assert np.array_equal([0x0000, 0x0000, 0x0000, 0x0000], autd.link().debug_values(dev.idx()))

        def f1(_: Device, gpio: GPIOOut) -> GPIOOutputTypeWrap | None:
            match gpio:
                case GPIOOut.O0:
                    return GPIOOutputType.Sync
                case GPIOOut.O1:
                    return GPIOOutputType.ModSegment
                case GPIOOut.O2:
                    return GPIOOutputType.ModIdx(0x01)
                case GPIOOut.O3:
                    return GPIOOutputType.StmSegment

        autd.send(GPIOOutputs(f1))
        for dev in autd.geometry():
            assert np.array_equal([0x10, 0x20, 0x21, 0x50], autd.link().debug_types(dev.idx()))
            assert np.array_equal([0x0000, 0x0000, 0x0001, 0x0000], autd.link().debug_values(dev.idx()))

        def f2(dev: Device, gpio: GPIOOut) -> GPIOOutputTypeWrap | None:
            match gpio:
                case GPIOOut.O0:
                    return GPIOOutputType.StmIdx(0x02)
                case GPIOOut.O1:
                    return GPIOOutputType.IsStmMode
                case GPIOOut.O2:
                    return GPIOOutputType.PwmOut(dev[3])
                case GPIOOut.O3:
                    return GPIOOutputType.Direct(True)  # noqa: FBT003

        autd.send(GPIOOutputs(f2))
        for dev in autd.geometry():
            assert np.array_equal([0x51, 0x52, 0xE0, 0xF0], autd.link().debug_types(dev.idx()))
            assert np.array_equal([0x0002, 0x0000, 0x0003, 0x0001], autd.link().debug_values(dev.idx()))

        sys_time = DcSysTime.now()

        def f3(_dev: Device, gpio: GPIOOut) -> GPIOOutputTypeWrap | None:
            match gpio:
                case GPIOOut.O0:
                    return GPIOOutputType.SysTimeEq(sys_time)
                case GPIOOut.O1:
                    return GPIOOutputType.SyncDiff
                case GPIOOut.O2:
                    return None
                case GPIOOut.O3:
                    return None

        autd.send(GPIOOutputs(f3))
        for dev in autd.geometry():
            assert np.array_equal([0x60, 0x70, 0x00, 0x00], autd.link().debug_types(dev.idx()))
            assert np.array_equal([(sys_time.sys_time() // 3125) >> 3, 0x00, 0x00, 0x00], autd.link().debug_values(dev.idx()))
