from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment, Static
from pyautd3.driver.datagram.segment import SwapSegment
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.modulation import Modulation, Sine
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_cache():
    autd1: Controller[Audit]
    autd2: Controller[Audit]
    with create_controller() as autd1, create_controller() as autd2:
        m1 = Sine(150 * Hz)
        m2 = Sine(150 * Hz).with_cache()
        assert m2.buffer is None

        autd1.send(m1)
        autd2.send(m2)

        for dev in autd1.geometry:
            mod_expect = autd1.link.modulation(dev.idx, Segment.S0)
            mod = autd2.link.modulation(dev.idx, Segment.S0)
            assert np.array_equal(mod, mod_expect)
            assert autd2.link.modulation_frequency_division(dev.idx, Segment.S0) == 10

        mod_expect = autd1.link.modulation(0, Segment.S0)
        assert m2.buffer is not None
        buf = np.fromiter((m for m in m2.buffer), dtype=np.uint8)
        assert np.array_equal(buf, mod_expect)


class CacheTest(Modulation["CacheTest"]):
    calc_cnt: int

    def __init__(self: "CacheTest") -> None:
        super().__init__(4000 * Hz)
        self.calc_cnt = 0

    def calc(self: "CacheTest"):
        self.calc_cnt += 1
        return np.array([0xFF] * 2)


def test_cache_check_once():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = CacheTest()
        autd.send(m)
        assert m.calc_cnt == 1
        autd.send(m)
        assert m.calc_cnt == 2

        m = CacheTest()
        m_cached = m.with_cache()

        autd.send(m_cached)
        assert m.calc_cnt == 1
        autd.send(m_cached)
        assert m.calc_cnt == 1


def test_transform():
    autd1: Controller[Audit]
    autd2: Controller[Audit]
    with create_controller() as autd1, create_controller() as autd2:
        m1 = Sine(150 * Hz)
        m2 = Sine(150 * Hz).with_transform(lambda _i, v: v // 2)

        autd1.send(m1)
        autd2.send(m2)

        for dev in autd1.geometry:
            mod_expect = autd1.link.modulation(dev.idx, Segment.S0)
            mod = autd2.link.modulation(dev.idx, Segment.S0)
            for i in range(len(mod_expect)):
                assert mod[i] == mod_expect[i] // 2
            assert autd2.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_radiation_pressure():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Sine(150 * Hz).with_radiation_pressure()

        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [
                180,
                200,
                217,
                231,
                242,
                250,
                254,
                254,
                251,
                245,
                235,
                222,
                206,
                187,
                165,
                141,
                115,
                87,
                58,
                28,
                0,
                28,
                58,
                87,
                115,
                141,
                165,
                187,
                206,
                222,
                235,
                245,
                251,
                254,
                254,
                250,
                242,
                231,
                217,
                200,
                180,
                157,
                133,
                106,
                78,
                48,
                16,
                0,
                39,
                68,
                97,
                124,
                150,
                173,
                194,
                212,
                227,
                239,
                248,
                253,
                255,
                253,
                248,
                239,
                227,
                212,
                194,
                173,
                150,
                124,
                97,
                68,
                39,
                0,
                16,
                48,
                78,
                106,
                133,
                157,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_mod_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link.current_mod_segment(0) == Segment.S0

        autd.send(Static.with_intensity(0x01))
        assert autd.link.current_mod_segment(0) == Segment.S0
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            assert np.all(mod == 0x01)
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S1)
            assert np.all(mod == 0xFF)

        autd.send(Static.with_intensity(0x02).with_segment(Segment.S1, TransitionMode.Immediate))
        assert autd.link.current_mod_segment(0) == Segment.S1
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            assert np.all(mod == 0x01)
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S1)
            assert np.all(mod == 0x02)

        autd.send(Static.with_intensity(0x03).with_segment(Segment.S0, None))
        assert autd.link.current_mod_segment(0) == Segment.S1
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            assert np.all(mod == 0x03)
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S1)
            assert np.all(mod == 0x02)

        autd.send(SwapSegment.Modulation(Segment.S0, TransitionMode.Immediate))
        assert autd.link.current_mod_segment(0) == Segment.S0
