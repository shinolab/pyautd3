from typing import TYPE_CHECKING

import pytest

from pyautd3 import (
    Controller,
    GainSTM,
    Null,
    ReadsFPGAState,
)
from pyautd3.autd_error import AUTDError
from pyautd3.driver.datagram.segment import SwapSegment
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.native_methods.autd3capi_driver import Segment
from tests.test_autd import create_controller, create_controller_async

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_fpga_state():
    autd: Controller[Audit]
    with create_controller() as autd:
        infos = autd.fpga_state()
        for info in infos:
            assert info is None

        autd.send(ReadsFPGAState(lambda _dev: True))
        autd.link.assert_thermal_sensor(0)
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert infos[0].is_thermal_assert
        assert infos[0].current_gain_segment == Segment.S0
        assert infos[0].current_mod_segment == Segment.S0
        assert infos[0].current_stm_segment is None
        assert infos[1] is not None
        assert not infos[1].is_thermal_assert
        assert infos[1].current_gain_segment == Segment.S0
        assert infos[1].current_mod_segment == Segment.S0
        assert infos[1].current_stm_segment is None

        autd.link.deassert_thermal_sensor(0)
        autd.link.assert_thermal_sensor(1)
        autd.send(SwapSegment.Modulation(Segment.S1, TransitionMode.Immediate))
        autd.send(SwapSegment.Gain(Segment.S1))
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert not infos[0].is_thermal_assert
        assert infos[0].current_gain_segment == Segment.S1
        assert infos[0].current_mod_segment == Segment.S1
        assert infos[0].current_stm_segment is None
        assert infos[1] is not None
        assert infos[1].is_thermal_assert
        assert infos[1].current_gain_segment == Segment.S1
        assert infos[1].current_mod_segment == Segment.S1
        assert infos[1].current_stm_segment is None

        autd.send(GainSTM(1.0 * Hz, [Null(), Null()]).with_segment(Segment.S0, TransitionMode.Immediate))
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert infos[0].current_gain_segment is None
        assert infos[0].current_stm_segment == Segment.S0
        assert infos[1] is not None
        assert infos[1].current_gain_segment is None
        assert infos[1].current_stm_segment == Segment.S0

        autd.send(GainSTM(1.0 * Hz, [Null(), Null()]).with_segment(Segment.S1, TransitionMode.Immediate))
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert infos[0].current_gain_segment is None
        assert infos[0].current_stm_segment == Segment.S1
        assert infos[1] is not None
        assert infos[1].current_gain_segment is None
        assert infos[1].current_stm_segment == Segment.S1

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            _ = autd.fpga_state()
        assert str(e.value) == "broken"
        autd.link.repair()


@pytest.mark.asyncio()
async def test_fpga_state_async():
    autd: Controller[Audit]
    with await create_controller_async() as autd:
        infos = await autd.fpga_state_async()
        for info in infos:
            assert info is None

        autd.send(ReadsFPGAState(lambda _dev: True))
        autd.link.assert_thermal_sensor(0)

        infos = await autd.fpga_state_async()
        assert infos[0] is not None
        assert infos[0].is_thermal_assert
        assert infos[1] is not None
        assert not infos[1].is_thermal_assert

        autd.link.deassert_thermal_sensor(0)
        autd.link.assert_thermal_sensor(1)

        infos = await autd.fpga_state_async()
        assert infos[0] is not None
        assert not infos[0].is_thermal_assert
        assert infos[1] is not None
        assert infos[1].is_thermal_assert

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            _ = await autd.fpga_state_async()
        assert str(e.value) == "broken"
        autd.link.repair()
