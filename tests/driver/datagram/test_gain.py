from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Device, Drive, EmitIntensity, Geometry, Phase, Segment, SwapSegment, Transducer
from pyautd3.gain import Gain, Uniform
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_cache():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Uniform((EmitIntensity(0x80), Phase(0x90))).with_cache())

        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x90)


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

        assert 0 not in g_cached.drives
        assert 1 in g_cached.drives

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)


def test_transform():
    autd: Controller[Audit]
    with create_controller() as autd:

        def transform(dev: Device) -> Callable[[Transducer, Drive], Drive]:
            if dev.idx == 0:
                return lambda _, d: Drive((Phase(d.phase.value + 32), d.intensity))
            return lambda _, d: Drive((Phase(d.phase.value - 32), d.intensity))

        autd.send(Uniform((EmitIntensity(0x80), Phase(128))).with_transform(transform))

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 128 + 32)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 128 - 32)


def test_transform_check_only_for_enabled():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.geometry[0].enable = False

        check = np.zeros(2, dtype=bool)

        def transform(dev: Device) -> Callable[[Transducer, Drive], Drive]:
            check[dev.idx] = True
            return lambda _, d: d

        autd.send(Uniform((EmitIntensity(0x80), Phase(0x90))).with_transform(transform))

        assert not check[0]
        assert check[1]

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
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
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x01)
            assert np.all(phases == 0x02)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x00)
            assert np.all(phases == 0x00)

        autd.send(Uniform((EmitIntensity(0x03), Phase(0x04))).with_segment(Segment.S1, transition=True))
        assert autd.link.current_stm_segment(0) == Segment.S1
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x01)
            assert np.all(phases == 0x02)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x03)
            assert np.all(phases == 0x04)

        autd.send(Uniform((EmitIntensity(0x05), Phase(0x06))).with_segment(Segment.S0, transition=False))
        assert autd.link.current_stm_segment(0) == Segment.S1
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x05)
            assert np.all(phases == 0x06)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x03)
            assert np.all(phases == 0x04)

        autd.send(SwapSegment.Gain(Segment.S0))
        assert autd.link.current_stm_segment(0) == Segment.S0
