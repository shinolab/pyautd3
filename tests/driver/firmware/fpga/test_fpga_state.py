from typing import TYPE_CHECKING

import pytest

from pyautd3 import Controller, GainSTM, Null, ReadsFPGAState, transition_mode
from pyautd3.autd_error import AUTDError
from pyautd3.driver.common.freq import Hz
from pyautd3.driver.datagram.segment import SwapSegmentGain, SwapSegmentModulation
from pyautd3.driver.datagram.stm.gain import GainSTMOption
from pyautd3.driver.datagram.with_segment import WithSegment
from pyautd3.native_methods.autd3 import Segment
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_fpga_state():
    autd: Controller[Audit]
    with create_controller() as autd:
        infos = autd.fpga_state()
        for info in infos:
            assert info is None

        autd.send(ReadsFPGAState(lambda _dev: True))
        autd.link().assert_thermal_sensor(0)
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert infos[0].is_thermal_assert()
        assert infos[0].current_gain_segment() == Segment.S0
        assert infos[0].current_mod_segment() == Segment.S0
        assert infos[0].current_stm_segment() is None
        assert infos[1] is not None
        assert not infos[1].is_thermal_assert()
        assert infos[1].current_gain_segment() == Segment.S0
        assert infos[1].current_mod_segment() == Segment.S0
        assert infos[1].current_stm_segment() is None

        autd.link().deassert_thermal_sensor(0)
        autd.link().assert_thermal_sensor(1)
        autd.send(SwapSegmentModulation(Segment.S1, transition_mode.Immediate()))
        autd.send(SwapSegmentGain(Segment.S1))
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert not infos[0].is_thermal_assert()
        assert infos[0].current_gain_segment() == Segment.S1
        assert infos[0].current_mod_segment() == Segment.S1
        assert infos[0].current_stm_segment() is None
        assert infos[1] is not None
        assert infos[1].is_thermal_assert()
        assert infos[1].current_gain_segment() == Segment.S1
        assert infos[1].current_mod_segment() == Segment.S1
        assert infos[1].current_stm_segment() is None

        autd.send(
            WithSegment(
                inner=GainSTM(gains=[Null(), Null()], config=1.0 * Hz, option=GainSTMOption()),
                segment=Segment.S0,
                transition_mode=transition_mode.Immediate(),
            ),
        )
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert infos[0].current_gain_segment() is None
        assert infos[0].current_stm_segment() == Segment.S0
        assert infos[1] is not None
        assert infos[1].current_gain_segment() is None
        assert infos[1].current_stm_segment() == Segment.S0

        autd.send(
            WithSegment(
                inner=GainSTM(gains=[Null(), Null()], config=1.0 * Hz, option=GainSTMOption()),
                segment=Segment.S1,
                transition_mode=transition_mode.Immediate(),
            ),
        )
        infos = autd.fpga_state()
        assert infos[0] is not None
        assert infos[0].current_gain_segment() is None
        assert infos[0].current_stm_segment() == Segment.S1
        assert infos[1] is not None
        assert infos[1].current_gain_segment() is None
        assert infos[1].current_stm_segment() == Segment.S1

        autd.link().break_down()
        with pytest.raises(AUTDError) as e:
            _ = autd.fpga_state()
        assert str(e.value) == "broken"
        autd.link().repair()
