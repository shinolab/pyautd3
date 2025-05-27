from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, FociSTM, Hz, LoopBehavior, SamplingConfig, Segment, Silencer
from pyautd3.driver.datagram.segment import SwapSegment
from pyautd3.driver.datagram.stm.control_point import ControlPoint, ControlPoints
from pyautd3.driver.datagram.with_loop_behavior import WithLoopBehavior
from pyautd3.driver.datagram.with_segment import WithSegment
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.utils import Duration
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_foci_stm():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        center = np.array([0.0, 0.0, 150.0])
        stm = FociSTM(foci=[center, center], config=1.0 * Hz)
        assert stm.sampling_config() == SamplingConfig(20000)
        autd.send(stm)
        for dev in autd.geometry():
            assert not autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_behavior(dev.idx(), Segment.S0) == LoopBehavior.Infinite
            assert autd.link().sound_speed(dev.idx(), Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 20000

        stm = FociSTM(foci=[center, center], config=1.0 * Hz).into_nearest()
        autd.send(stm)
        for dev in autd.geometry():
            assert not autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_behavior(dev.idx(), Segment.S0) == LoopBehavior.Infinite
            assert autd.link().sound_speed(dev.idx(), Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 20000

        stm = FociSTM(foci=[center, center], config=Duration.from_secs(1))
        autd.send(stm)
        for dev in autd.geometry():
            assert not autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_behavior(dev.idx(), Segment.S0) == LoopBehavior.ONCE
            assert autd.link().sound_speed(dev.idx(), Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 20000

        stm = FociSTM(foci=[center, center], config=Duration.from_secs(1)).into_nearest()
        autd.send(stm)
        for dev in autd.geometry():
            assert not autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_behavior(dev.idx(), Segment.S0) == LoopBehavior.ONCE
            assert autd.link().sound_speed(dev.idx(), Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 20000

        stm = FociSTM(foci=[center, center], config=SamplingConfig(1))
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 1
        for dev in autd.geometry():
            assert autd.link().stm_cycle(dev.idx(), Segment.S0) == 2
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 1)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        stm = FociSTM(foci=[ControlPoint(point=center), ControlPoint(point=center)], config=SamplingConfig(1))
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_divide(dev.idx(), Segment.S0) == 1
        for dev in autd.geometry():
            assert autd.link().stm_cycle(dev.idx(), Segment.S0) == 2
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 1)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)


def test_foci_stm_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link().current_stm_segment(0) == Segment.S0

        autd.send(
            FociSTM(
                foci=[np.zeros(3), np.zeros(3)],
                config=SamplingConfig(0x1234),
            ),
        )
        assert autd.link().current_stm_segment(0) == Segment.S0
        assert autd.link().stm_cycle(0, Segment.S0) == 2
        assert autd.link().stm_freqency_divide(0, Segment.S0) == 0x1234

        autd.send(
            WithSegment(
                inner=FociSTM(
                    foci=[np.zeros(3), np.zeros(3)],
                    config=SamplingConfig(0xDEF0),
                ),
                segment=Segment.S1,
                transition_mode=TransitionMode.Immediate,
            ),
        )
        assert autd.link().current_stm_segment(0) == Segment.S1
        assert autd.link().stm_cycle(0, Segment.S1) == 2
        assert autd.link().stm_freqency_divide(0, Segment.S1) == 0xDEF0

        autd.send(
            WithSegment(
                inner=FociSTM(
                    foci=[np.zeros(3), np.zeros(3), np.zeros(3)],
                    config=SamplingConfig(0x8765),
                ),
                segment=Segment.S0,
                transition_mode=None,
            ),
        )
        assert autd.link().current_stm_segment(0) == Segment.S1
        assert autd.link().stm_cycle(0, Segment.S0) == 3
        assert autd.link().stm_freqency_divide(0, Segment.S0) == 0x8765

        autd.send(SwapSegment.FociSTM(Segment.S0, TransitionMode.Immediate))
        assert autd.link().current_stm_segment(0) == Segment.S0


def test_foci_stm_loop_behavior():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(
            WithLoopBehavior(
                inner=FociSTM(
                    foci=[np.zeros(3), np.zeros(3)],
                    config=SamplingConfig(0xDEF0),
                ),
                segment=Segment.S1,
                transition_mode=TransitionMode.SyncIdx,
                loop_behavior=LoopBehavior.ONCE,
            ),
        )
        assert autd.link().stm_cycle(0, Segment.S1) == 2
        assert autd.link().stm_freqency_divide(0, Segment.S1) == 0xDEF0
        assert autd.link().stm_loop_behavior(0, Segment.S1) == LoopBehavior.ONCE


def foci_stm_n(n: int) -> None:
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci = [ControlPoints(points=[center] * n, intensity=EmitIntensity(i)) for i in range(size)]

        stm = FociSTM(foci=foci, config=1.0 * Hz)
        autd.send(stm)
        for dev in autd.geometry():
            for i in range(size):
                intensities, _ = autd.link().drives_at(dev.idx(), Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM(foci=foci, config=1.0 * Hz).into_nearest()
        autd.send(stm)
        for dev in autd.geometry():
            for i in range(size):
                intensities, _ = autd.link().drives_at(dev.idx(), Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM(foci=foci, config=Duration.from_secs(1))
        autd.send(stm)
        for dev in autd.geometry():
            for i in range(size):
                intensities, _ = autd.link().drives_at(dev.idx(), Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM(foci=foci, config=Duration.from_secs(1)).into_nearest()
        autd.send(stm)
        for dev in autd.geometry():
            for i in range(size):
                intensities, _ = autd.link().drives_at(dev.idx(), Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM(foci=foci, config=SamplingConfig.FREQ_40K)
        autd.send(stm)
        for dev in autd.geometry():
            for i in range(size):
                intensities, _ = autd.link().drives_at(dev.idx(), Segment.S0, i)
                assert np.all(intensities == i)

        with pytest.raises(TypeError):
            _ = FociSTM(foci=foci, config=SamplingConfig.FREQ_40K).into_nearest()


def test_foci_stm_1():
    foci_stm_n(1)


def test_foci_stm_2():
    foci_stm_n(2)


def test_foci_stm_3():
    foci_stm_n(3)


def test_foci_stm_4():
    foci_stm_n(4)


def test_foci_stm_5():
    foci_stm_n(5)


def test_foci_stm_6():
    foci_stm_n(6)


def test_foci_stm_7():
    foci_stm_n(7)


def test_foci_stm_8():
    foci_stm_n(8)


def test_foci_stm_mix():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        center = autd.center() + np.array([0.0, 0.0, 150.0])

        stm = FociSTM(foci=[ControlPoints(points=[center]), ControlPoints(points=[center, center])], config=1.0 * Hz)
        with pytest.raises(ValueError):  # noqa: PT011
            autd.send(stm)

        stm = FociSTM(foci=[ControlPoints(points=[center] * 9), ControlPoints(points=[center] * 9)], config=1.0 * Hz)
        with pytest.raises(ValueError):  # noqa: PT011
            autd.send(stm)
