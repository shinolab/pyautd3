from typing import TYPE_CHECKING

import pytest

from pyautd3 import (
    ConfigureDebugOutputIdx,
    Controller,
)
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_debug_output_idx():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.debug_output_idx(dev.idx) == 0xFF

        await autd.send_async(ConfigureDebugOutputIdx(lambda dev: dev[0]))

        for dev in autd.geometry:
            assert autd.link.debug_output_idx(dev.idx) == 0

        await autd.send_async(ConfigureDebugOutputIdx(lambda dev: dev[10] if dev.idx == 0 else None))

        assert autd.link.debug_output_idx(0) == 10
        assert autd.link.debug_output_idx(1) == 0xFF
