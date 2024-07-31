from datetime import timedelta
from typing import TYPE_CHECKING

import numpy as np

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
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
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
            1.0 * Hz,
            (center + radius * np.array([np.cos(theta), np.sin(theta), 0]) for theta in (2.0 * np.pi * i / size for i in range(size))),
        ).with_loop_behavior(LoopBehavior.Once)
        assert stm.freq == 1.0 * Hz
        assert stm.period == timedelta(seconds=1.0)
        assert stm.sampling_config == SamplingConfig(20000)
        autd.send(stm)
        for dev in autd.geometry:
            assert not autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
            assert autd.link.sound_speed(dev.idx, Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 20000

        stm = FociSTM.nearest(1.0 * Hz, [center, center])
        autd.send(stm)
        for dev in autd.geometry:
            assert not autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
            assert autd.link.sound_speed(dev.idx, Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 20000

        stm = FociSTM(timedelta(seconds=1.0), [center, center])
        autd.send(stm)
        for dev in autd.geometry:
            assert not autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
            assert autd.link.sound_speed(dev.idx, Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 20000

        stm = FociSTM.nearest(timedelta(seconds=1.0), [center, center])
        autd.send(stm)
        for dev in autd.geometry:
            assert not autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
            assert autd.link.sound_speed(dev.idx, Segment.S0) == int(dev.sound_speed / 1000.0 * 64.0)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 20000

        stm = FociSTM(SamplingConfig(1), [center, center])
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 1
        for dev in autd.geometry:
            assert autd.link.stm_cycle(dev.idx, Segment.S0) == 2
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)


def test_foci_stm_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link.current_stm_segment(0) == Segment.S0

        autd.send(
            FociSTM(
                SamplingConfig(0x1234),
                [np.zeros(3), np.zeros(3)],
            ),
        )
        assert autd.link.current_stm_segment(0) == Segment.S0
        assert autd.link.stm_cycle(0, Segment.S0) == 2
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0x1234

        autd.send(
            FociSTM(
                SamplingConfig(0xDEF0),
                [np.zeros(3), np.zeros(3)],
            ).with_segment(Segment.S1, TransitionMode.Immediate),
        )
        assert autd.link.current_stm_segment(0) == Segment.S1
        assert autd.link.stm_cycle(0, Segment.S1) == 2
        assert autd.link.stm_freqency_division(0, Segment.S1) == 0xDEF0

        autd.send(
            FociSTM(
                SamplingConfig(0x8765),
                [np.zeros(3), np.zeros(3), np.zeros(3)],
            ).with_segment(Segment.S0, None),
        )
        assert autd.link.current_stm_segment(0) == Segment.S1
        assert autd.link.stm_cycle(0, Segment.S0) == 3
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0x8765

        autd.send(SwapSegment.FociSTM(Segment.S0, TransitionMode.Immediate))
        assert autd.link.current_stm_segment(0) == Segment.S0


def foci_stm_n(control_points):  # noqa: ANN001
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = len(control_points)
        stm = FociSTM(
            1.0 * Hz,
            control_points,
        )
        autd.send(stm)
        for dev in autd.geometry:
            for i in range(size):
                intensities, _ = autd.link.drives(dev.idx, Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM.nearest(1.0 * Hz, control_points)
        autd.send(stm)
        for dev in autd.geometry:
            for i in range(size):
                intensities, _ = autd.link.drives(dev.idx, Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM(
            timedelta(seconds=1.0),
            control_points,
        )
        autd.send(stm)
        for dev in autd.geometry:
            for i in range(size):
                intensities, _ = autd.link.drives(dev.idx, Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM.nearest(
            timedelta(seconds=1.0),
            control_points,
        )
        autd.send(stm)
        for dev in autd.geometry:
            for i in range(size):
                intensities, _ = autd.link.drives(dev.idx, Segment.S0, i)
                assert np.all(intensities == i)

        stm = FociSTM(SamplingConfig(10), control_points)
        autd.send(stm)
        for dev in autd.geometry:
            for i in range(size):
                intensities, _ = autd.link.drives(dev.idx, Segment.S0, i)
                assert np.all(intensities == i)


def test_foci_stm_1():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints1(center).with_intensity(i) for i in range(size)])
        foci_stm_n([ControlPoints1(ControlPoint(center)).with_intensity(i) for i in range(size)])


def test_foci_stm_2():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints2((center, center)).with_intensity(i) for i in range(size)])
        foci_stm_n([ControlPoints2((ControlPoint(center), ControlPoint(center))).with_intensity(i) for i in range(size)])


def test_foci_stm_3():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints3((center, center, center)).with_intensity(i) for i in range(size)])
        foci_stm_n([ControlPoints3((ControlPoint(center), ControlPoint(center), ControlPoint(center))).with_intensity(i) for i in range(size)])


def test_foci_stm_4():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints4((center, center, center, center)).with_intensity(i) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints4((ControlPoint(center), ControlPoint(center), ControlPoint(center), ControlPoint(center))).with_intensity(i)
                for i in range(size)
            ],
        )


def test_foci_stm_5():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints5((center, center, center, center, center)).with_intensity(i) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints5(
                    (ControlPoint(center), ControlPoint(center), ControlPoint(center), ControlPoint(center), ControlPoint(center)),
                ).with_intensity(i)
                for i in range(size)
            ],
        )


def test_foci_stm_6():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints6((center, center, center, center, center, center)).with_intensity(i) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints6(
                    (
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                    ),
                ).with_intensity(i)
                for i in range(size)
            ],
        )


def test_foci_stm_7():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints7((center, center, center, center, center, center, center)).with_intensity(i) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints7(
                    (
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                    ),
                ).with_intensity(i)
                for i in range(size)
            ],
        )


def test_foci_stm_8():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 100
        center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
        foci_stm_n([ControlPoints8((center, center, center, center, center, center, center, center)).with_intensity(i) for i in range(size)])
        foci_stm_n(
            [
                ControlPoints8(
                    (
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                        ControlPoint(center),
                    ),
                ).with_intensity(i)
                for i in range(size)
            ],
        )
