from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, EmitIntensity, LoopBehavior, SamplingConfiguration, Segment
from pyautd3.modulation import Modulation, Sine
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_cache():
    autd1: Controller[Audit]
    autd2: Controller[Audit]
    with await create_controller() as autd1, await create_controller() as autd2:
        m1 = Sine(150)
        m2 = Sine(150).with_cache()
        assert m2.buffer is None

        assert await autd1.send_async(m1)
        assert await autd2.send_async(m2)

        for dev in autd1.geometry:
            mod_expect = autd1.link.modulation(dev.idx, Segment.S0)
            mod = autd2.link.modulation(dev.idx, Segment.S0)
            assert np.array_equal(mod, mod_expect)
            assert autd2.link.modulation_frequency_division(dev.idx, Segment.S0) == 5120

        mod_expect = autd1.link.modulation(0, Segment.S0)
        assert m2.buffer is not None
        buf = np.fromiter((m.value for m in m2.buffer), dtype=np.uint8)
        assert np.array_equal(buf, mod_expect)


class CacheTest(Modulation):
    calc_cnt: int

    def __init__(self: "CacheTest") -> None:
        super().__init__(SamplingConfiguration.from_frequency(4e3), LoopBehavior.infinite())
        self.calc_cnt = 0

    def calc(self: "CacheTest"):
        self.calc_cnt += 1
        return np.array([EmitIntensity(0xFF)] * 2)


@pytest.mark.asyncio()
async def test_cache_check_once():
    autd: Controller[Audit]
    with await create_controller() as autd:
        m = CacheTest()
        assert await autd.send_async(m)
        assert m.calc_cnt == 1
        assert await autd.send_async(m)
        assert m.calc_cnt == 2

        m = CacheTest()
        m_cached = m.with_cache()

        assert await autd.send_async(m_cached)
        assert m.calc_cnt == 1
        assert await autd.send_async(m_cached)
        assert m.calc_cnt == 1


@pytest.mark.asyncio()
async def test_transform():
    autd1: Controller[Audit]
    autd2: Controller[Audit]
    with await create_controller() as autd1, await create_controller() as autd2:
        m1 = Sine(150)
        m2 = Sine(150).with_transform(lambda _i, v: EmitIntensity(v.value // 2))

        assert await autd1.send_async(m1)
        assert await autd2.send_async(m2)

        for dev in autd1.geometry:
            mod_expect = autd1.link.modulation(dev.idx, Segment.S0)
            mod = autd2.link.modulation(dev.idx, Segment.S0)
            for i in range(len(mod_expect)):
                assert mod[i] == mod_expect[i] // 2
            assert autd2.link.modulation_frequency_division(dev.idx, Segment.S0) == 5120


@pytest.mark.asyncio()
async def test_radiation_pressure():
    autd: Controller[Audit]
    with await create_controller() as autd:
        m = Sine(150).with_radiation_pressure()

        assert await autd.send_async(m)

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
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 5120
