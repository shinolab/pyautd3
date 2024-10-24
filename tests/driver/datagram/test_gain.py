from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Device, Drive, EmitIntensity, Geometry, Phase, Segment, SwapSegment, Transducer
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.gain import Gain, Uniform
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_cache():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Uniform((EmitIntensity(0x80), Phase(0x90))).with_cache())

        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x90)

    _ = Uniform((EmitIntensity(0x80), Phase(0x90))).with_cache()


class CacheTest(Gain["CacheTest"]):
    calc_cnt: int

    def __init__(self: "CacheTest") -> None:
        self.calc_cnt = 0

    def calc(self: "CacheTest", _: Geometry) -> Callable[[Device], Callable[[Transducer], Drive | EmitIntensity | Phase | tuple]]:
        self.calc_cnt += 1
        return Gain._transform(lambda _dev: lambda _tr: Drive((Phase(0x90), EmitIntensity(0x80))))


def test_cache_check_once():
    autd: Controller[Audit]
    with create_controller() as autd:
        g = CacheTest()
        autd.send(g)
        assert g.calc_cnt == 1
        autd.send(g)
        assert g.calc_cnt == 2

        g = CacheTest()
        g_cached = g.with_cache()
        autd.send(g_cached)
        assert g.calc_cnt == 1
        autd.send(g_cached)
        assert g.calc_cnt == 1


def test_cache_check_only_for_enabled():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.geometry[0].enable = False

        g = CacheTest()
        g_cached = g.with_cache()
        autd.send(g_cached)

        intensities, phases = autd.link.drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        intensities, phases = autd.link.drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)


def test_gain_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link.current_stm_segment(0) == Segment.S0

        autd.send(Uniform((EmitIntensity(0x01), Phase(0x02))))
        assert autd.link.current_stm_segment(0) == Segment.S0
        assert autd.link.stm_cycle(0, Segment.S0) == 1
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0xFFFF
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x01)
            assert np.all(phases == 0x02)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x00)
            assert np.all(phases == 0x00)

        autd.send(Uniform((EmitIntensity(0x03), Phase(0x04))).with_segment(Segment.S1, TransitionMode.Immediate))
        assert autd.link.current_stm_segment(0) == Segment.S1
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x01)
            assert np.all(phases == 0x02)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x03)
            assert np.all(phases == 0x04)

        autd.send(Uniform((EmitIntensity(0x05), Phase(0x06))).with_segment(Segment.S0, None))
        assert autd.link.current_stm_segment(0) == Segment.S1
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x05)
            assert np.all(phases == 0x06)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x03)
            assert np.all(phases == 0x04)

        autd.send(SwapSegment.Gain(Segment.S0, TransitionMode.Immediate))
        assert autd.link.current_stm_segment(0) == Segment.S0
