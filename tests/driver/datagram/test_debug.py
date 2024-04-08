from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import (
    ConfigureDebugSettings,
    Controller,
    DebugType,
)
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_debug_output_idx():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert np.array_equal([0x00, 0x00, 0x00, 0x00], autd.link.debug_types(dev.idx))
            assert np.array_equal([0x0000, 0x0000, 0x0000, 0x0000], autd.link.debug_values(dev.idx))

        await autd.send_async(
            ConfigureDebugSettings(lambda _dev: [DebugType.Disable(), DebugType.BaseSignal(), DebugType.Thermo(), DebugType.ForceFan()]),
        )
        for dev in autd.geometry:
            assert np.array_equal([0x00, 0x01, 0x02, 0x03], autd.link.debug_types(dev.idx))
            assert np.array_equal([0x0000, 0x0000, 0x0000, 0x0000], autd.link.debug_values(dev.idx))

        await autd.send_async(
            ConfigureDebugSettings(lambda _dev: [DebugType.Sync(), DebugType.ModSegment(), DebugType.ModIdx(0x01), DebugType.StmSegment()]),
        )
        for dev in autd.geometry:
            assert np.array_equal([0x10, 0x20, 0x21, 0x50], autd.link.debug_types(dev.idx))
            assert np.array_equal([0x0000, 0x0000, 0x0001, 0x0000], autd.link.debug_values(dev.idx))

        await autd.send_async(
            ConfigureDebugSettings(
                lambda dev: [DebugType.StmIdx(0x02), DebugType.IsStmMode(), DebugType.PwmOut(dev[3]), DebugType.Direct(value=True)],
            ),
        )
        for dev in autd.geometry:
            assert np.array_equal([0x51, 0x52, 0xE0, 0xF0], autd.link.debug_types(dev.idx))
            assert np.array_equal([0x0002, 0x0000, 0x0003, 0x0001], autd.link.debug_values(dev.idx))
