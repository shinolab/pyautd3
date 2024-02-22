from typing import TYPE_CHECKING

import pytest

from pyautd3 import (
    ConfigureReadsFPGAState,
    Controller,
    GainSTM,
    Null,
)
from pyautd3.autd_error import AUTDError
from pyautd3.driver.datagram.gain.gain import ChangeGainSegment
from pyautd3.driver.datagram.modulation.modulation import ChangeModulationSegment
from pyautd3.native_methods.autd3capi_def import Segment
from tests.test_autd import create_controller, create_controller_sync

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_fpga_state():
    autd: Controller[Audit]
    with create_controller_sync() as autd:
        infos = autd.fpga_state()
        for info in infos:
            assert info is None

        autd.send(ConfigureReadsFPGAState(lambda _dev: True))
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
        autd.send(ChangeModulationSegment(Segment.S1))
        autd.send(ChangeGainSegment(Segment.S1))
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

        autd.send(GainSTM.from_freq(1.0).add_gains_from_iter([Null(), Null()]).with_segment(Segment.S0, update_segment=True))
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert infos[0].current_gain_segment is None
        assert infos[0].current_stm_segment == Segment.S0
        assert infos[1] is not None
        assert infos[1].current_gain_segment is None
        assert infos[1].current_stm_segment == Segment.S0

        autd.send(GainSTM.from_freq(1.0).add_gains_from_iter([Null(), Null()]).with_segment(Segment.S1, update_segment=True))
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


@pytest.mark.asyncio()
async def test_fpga_state_async():
    autd: Controller[Audit]
    with await create_controller() as autd:
        infos = await autd.fpga_state_async()
        for info in infos:
            assert info is None

        autd.send(ConfigureReadsFPGAState(lambda _dev: True))
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
