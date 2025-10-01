from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, GainSTM, GainSTMMode, Hz, SamplingConfig, Segment, Silencer, Uniform, transition_mode
from pyautd3.driver.datagram.segment import SwapSegmentGainSTM
from pyautd3.driver.datagram.stm.gain import GainSTMOption
from pyautd3.driver.datagram.with_finite_loop import WithFiniteLoop
from pyautd3.driver.datagram.with_segment import WithSegment
from pyautd3.driver.firmware.fpga.emit_intensity import Intensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.utils import Duration
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_gain_stm():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 2
        stm = GainSTM(
            gains=(Uniform(intensity=Intensity(0xFF // (i + 1)), phase=Phase(0)) for i in range(size)),
            config=1.0 * Hz,
            option=GainSTMOption(),
        )
        assert stm.sampling_config() == SamplingConfig(20000)
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_count(dev.idx(), Segment.S0) == 0xFFFF
        for dev in autd.geometry():
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 20000

        stm = GainSTM(
            gains=[Uniform(intensity=Intensity(0xFF), phase=Phase(0)), Uniform(intensity=Intensity(0x80), phase=Phase(0))],
            config=1.0 * Hz,
            option=GainSTMOption(),
        ).into_nearest()
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_count(dev.idx(), Segment.S0) == 0xFFFF
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 20000

        stm = GainSTM(
            gains=[Uniform(intensity=Intensity(0xFF), phase=Phase(0)), Uniform(intensity=Intensity(0x80), phase=Phase(0))],
            config=Duration.from_secs(1),
            option=GainSTMOption(),
        )
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_count(dev.idx(), Segment.S0) == 0xFFFF
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 20000

        stm = GainSTM(
            gains=[Uniform(intensity=Intensity(0xFF), phase=Phase(0)), Uniform(intensity=Intensity(0x80), phase=Phase(0))],
            config=Duration.from_secs(1),
            option=GainSTMOption(),
        ).into_nearest()
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_count(dev.idx(), Segment.S0) == 0xFFFF
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 20000

        stm = GainSTM(
            gains=[Uniform(intensity=Intensity(0xFF), phase=Phase(0)), Uniform(intensity=Intensity(0x80), phase=Phase(0))],
            config=SamplingConfig(1),
            option=GainSTMOption(),
        )
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 1
            assert autd.link().stm_cycle(dev.idx(), Segment.S0) == 2
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 1)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        stm = GainSTM(
            gains=[Uniform(intensity=Intensity(0xFF), phase=Phase(0)), Uniform(intensity=Intensity(0x80), phase=Phase(0))],
            config=SamplingConfig(1),
            option=GainSTMOption(mode=GainSTMMode.PhaseFull),
        )
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().stm_cycle(dev.idx(), Segment.S0) == 2
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 1)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        stm = GainSTM(
            gains=[Uniform(intensity=Intensity(0xFF), phase=Phase(0)), Uniform(intensity=Intensity(0x80), phase=Phase(0))],
            config=SamplingConfig(1),
            option=GainSTMOption(mode=GainSTMMode.PhaseHalf),
        )
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().stm_cycle(dev.idx(), Segment.S0) == 2
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 1)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        with pytest.raises(TypeError):
            _ = GainSTM(
                gains=[Uniform(intensity=Intensity(0xFF), phase=Phase(0)), Uniform(intensity=Intensity(0x80), phase=Phase(0))],
                config=SamplingConfig(1),
                option=GainSTMOption(mode=GainSTMMode.PhaseHalf),
            ).into_nearest()


def test_gain_stm_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link().current_stm_segment(0) == Segment.S0

        autd.send(
            GainSTM(
                gains=[Uniform(intensity=Intensity(0x01), phase=Phase(0)), Uniform(intensity=Intensity(0x02), phase=Phase(0))],
                config=SamplingConfig(0x1234),
                option=GainSTMOption(),
            ),
        )
        assert autd.link().current_stm_segment(0) == Segment.S0
        assert autd.link().stm_cycle(0, Segment.S0) == 2
        assert autd.link().stm_freqency_divide(0, Segment.S0) == 0x1234
        for dev in autd.geometry():
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S0, 0)[0] == 0x01)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S0, 1)[0] == 0x02)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S1, 0)[0] == 0x00)

        autd.send(
            WithSegment(
                inner=GainSTM(
                    gains=[Uniform(intensity=Intensity(0x03), phase=Phase(0)), Uniform(intensity=Intensity(0x04), phase=Phase(0))],
                    config=SamplingConfig(0x9ABC),
                    option=GainSTMOption(),
                ),
                segment=Segment.S1,
                transition_mode=transition_mode.Immediate(),
            ),
        )
        assert autd.link().current_stm_segment(0) == Segment.S1
        assert autd.link().stm_cycle(0, Segment.S1) == 2
        assert autd.link().stm_freqency_divide(0, Segment.S1) == 0x9ABC
        for dev in autd.geometry():
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S0, 0)[0] == 0x01)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S0, 1)[0] == 0x02)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S1, 0)[0] == 0x03)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S1, 1)[0] == 0x04)

        autd.send(
            WithSegment(
                inner=GainSTM(
                    gains=[
                        Uniform(intensity=Intensity(0x05), phase=Phase(0)),
                        Uniform(intensity=Intensity(0x06), phase=Phase(0)),
                        Uniform(intensity=Intensity(0x07), phase=Phase(0)),
                    ],
                    config=SamplingConfig(0x4321),
                    option=GainSTMOption(),
                ),
                segment=Segment.S0,
                transition_mode=transition_mode.Later(),
            ),
        )
        assert autd.link().current_stm_segment(0) == Segment.S1
        assert autd.link().stm_cycle(0, Segment.S0) == 3
        assert autd.link().stm_freqency_divide(0, Segment.S0) == 0x4321
        for dev in autd.geometry():
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S0, 0)[0] == 0x05)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S0, 1)[0] == 0x06)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S0, 2)[0] == 0x07)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S1, 0)[0] == 0x03)
            assert np.all(autd.link().drives_at(dev.idx(), Segment.S1, 1)[0] == 0x04)

        autd.send(SwapSegmentGainSTM(Segment.S0, transition_mode.Immediate()))
        assert autd.link().current_stm_segment(0) == Segment.S0


def test_foci_stm_loop_count():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(
            WithFiniteLoop(
                inner=GainSTM(
                    gains=[Uniform(intensity=Intensity(0x01), phase=Phase(0)), Uniform(intensity=Intensity(0x02), phase=Phase(0))],
                    config=SamplingConfig(0xDEF0),
                    option=GainSTMOption(),
                ),
                segment=Segment.S1,
                transition_mode=transition_mode.SyncIdx(),
                loop_count=1,
            ),
        )
        assert autd.link().stm_cycle(0, Segment.S1) == 2
        assert autd.link().stm_freqency_divide(0, Segment.S1) == 0xDEF0
        assert autd.link().stm_loop_count(0, Segment.S1) == 0
