from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, ControlPoint, FociSTM, Hz, LoopBehavior, SamplingConfig, Segment, Silencer
from pyautd3.driver.datagram.segment import SwapSegment
from pyautd3.driver.datagram.stm.control_point import (
    ControlPoints1,
    ControlPoints2,
    ControlPoints3,
    ControlPoints4,
    ControlPoints5,
    ControlPoints6,
    ControlPoints7,
    ControlPoints8,
)
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

        radius = 30.0
        size = 2
        center = np.array([0.0, 0.0, 150.0])
        stm = FociSTM(
            foci=(center + radius * np.array([np.cos(theta), np.sin(theta), 0]) for theta in (2.0 * np.pi * i / size for i in range(size))),
            config=1.0 * Hz,
        )
        assert stm.sampling_config() == SamplingConfig(20000)
        autd.send(stm)
        for dev in autd.geometry():
            assert not autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_behavior(dev.idx(), Segment.S0) == LoopBehavior.Infinite
            assert autd.link().sound_speed(dev.idx(), Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_division(dev.idx(), Segment.S0) == 20000

        stm = FociSTM(foci=[center, center], config=1.0 * Hz).into_nearest()
        autd.send(stm)
        for dev in autd.geometry():
            assert not autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_behavior(dev.idx(), Segment.S0) == LoopBehavior.Infinite
            assert autd.link().sound_speed(dev.idx(), Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_division(dev.idx(), Segment.S0) == 20000

        stm = FociSTM(foci=[center, center], config=Duration.from_secs(1))
        autd.send(stm)
        for dev in autd.geometry():
            assert not autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_behavior(dev.idx(), Segment.S0) == LoopBehavior.ONCE
            assert autd.link().sound_speed(dev.idx(), Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_division(dev.idx(), Segment.S0) == 20000

        stm = FociSTM(foci=[center, center], config=Duration.from_secs(1)).into_nearest()
        autd.send(stm)
        for dev in autd.geometry():
            assert not autd.link().is_stm_gain_mode(dev.idx(), Segment.S0)
            assert autd.link().stm_loop_behavior(dev.idx(), Segment.S0) == LoopBehavior.ONCE
            assert autd.link().sound_speed(dev.idx(), Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_division(dev.idx(), Segment.S0) == 20000

        stm = FociSTM(foci=[center, center], config=SamplingConfig(1))
        autd.send(stm)
        for dev in autd.geometry():
            assert autd.link().stm_freqency_division(dev.idx(), Segment.S0) == 1
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
        assert autd.link().stm_freqency_division(0, Segment.S0) == 0x1234

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
        assert autd.link().stm_freqency_division(0, Segment.S1) == 0xDEF0

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
        assert autd.link().stm_freqency_division(0, Segment.S0) == 0x8765

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
        assert autd.link().stm_freqency_division(0, Segment.S1) == 0xDEF0
        assert autd.link().stm_loop_behavior(0, Segment.S1) == LoopBehavior.ONCE


def foci_stm_n(foci):  # noqa: ANN001
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = len(foci)
        stm = FociSTM(
            foci=foci,
            config=1.0 * Hz,
        )
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

        stm = FociSTM(
            foci=foci,
            config=Duration.from_secs(1),
        )
        autd.send(stm)
        for dev in autd.geometry():
            for i in range(size):
                intensities, _ = autd.link().drives_at(dev.idx(), Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM(
            foci=foci,
            config=Duration.from_secs(1),
        ).into_nearest()
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
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints1(points=center, intensity=EmitIntensity(i)) for i in range(size)])
        foci_stm_n([ControlPoints1(points=ControlPoint(point=center), intensity=EmitIntensity(i)) for i in range(size)])


def test_foci_stm_2():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints2(points=(center, center), intensity=EmitIntensity(i)) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints2(
                    points=(ControlPoint(point=center), ControlPoint(point=center)),
                    intensity=EmitIntensity(i),
                )
                for i in range(size)
            ],
        )


def test_foci_stm_3():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints3(points=(center, center, center), intensity=EmitIntensity(i)) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints3(
                    points=(ControlPoint(point=center), ControlPoint(point=center), ControlPoint(point=center)),
                    intensity=EmitIntensity(i),
                )
                for i in range(size)
            ],
        )


def test_foci_stm_4():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints4(points=(center, center, center, center), intensity=EmitIntensity(i)) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints4(
                    points=(ControlPoint(point=center), ControlPoint(point=center), ControlPoint(point=center), ControlPoint(point=center)),
                    intensity=EmitIntensity(i),
                )
                for i in range(size)
            ],
        )


def test_foci_stm_5():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints5(points=(center, center, center, center, center), intensity=EmitIntensity(i)) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints5(
                    points=(
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                    ),
                    intensity=EmitIntensity(i),
                )
                for i in range(size)
            ],
        )


def test_foci_stm_6():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci_stm_n(
            [
                ControlPoints6(
                    points=(center, center, center, center, center, center),
                    intensity=EmitIntensity(i),
                )
                for i in range(size)
            ],
        )
        foci_stm_n(
            [
                ControlPoints6(
                    points=(
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                    ),
                    intensity=EmitIntensity(i),
                )
                for i in range(size)
            ],
        )


def test_foci_stm_7():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints7(points=(center, center, center, center, center, center, center), intensity=EmitIntensity(i)) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints7(
                    points=(
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                    ),
                    intensity=EmitIntensity(i),
                )
                for i in range(size)
            ],
        )


def test_foci_stm_8():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.center() + np.array([0.0, 0.0, 150.0])
        foci_stm_n(
            [
                ControlPoints8(points=(center, center, center, center, center, center, center, center), intensity=EmitIntensity(i))
                for i in range(size)
            ],
        )
        foci_stm_n(
            [
                ControlPoints8(
                    points=(
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                        ControlPoint(point=center),
                    ),
                    intensity=EmitIntensity(i),
                )
                for i in range(size)
            ],
        )
