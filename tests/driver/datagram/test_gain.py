from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import ChangeGainSegment, Controller, Device, Drive, EmitIntensity, Geometry, Phase, Segment, Transducer
from pyautd3.driver.datagram.gain import IGainWithCache
from pyautd3.gain import Gain, Uniform
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_cache():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert await autd.send_async(Uniform(0x80).with_phase(Phase(0x90)).with_cache())

        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x90)


class CacheTest(IGainWithCache, Gain):
    calc_cnt: int

    def __init__(self: "CacheTest") -> None:
        self.calc_cnt = 0

    def calc(self: "CacheTest", geometry: Geometry) -> dict[int, np.ndarray]:
        self.calc_cnt += 1
        return Gain._transform(
            geometry,
            lambda _dev, _tr: Drive(
                Phase(0x90),
                EmitIntensity(0x80),
            ),
        )


@pytest.mark.asyncio()
async def test_cache_check_once():
    autd: Controller[Audit]
    with await create_controller() as autd:
        g = CacheTest()
        assert await autd.send_async(g)
        assert g.calc_cnt == 1
        assert await autd.send_async(g)
        assert g.calc_cnt == 2

        g = CacheTest()
        g_cached = g.with_cache()
        assert await autd.send_async(g_cached)
        assert g.calc_cnt == 1
        assert await autd.send_async(g_cached)
        assert g.calc_cnt == 1


@pytest.mark.asyncio()
async def test_cache_check_only_for_enabled():
    autd: Controller[Audit]
    with await create_controller() as autd:
        autd.geometry[0].enable = False

        g = CacheTest()
        g_cached = g.with_cache()
        assert await autd.send_async(g_cached)

        assert 0 not in g_cached.drives
        assert 1 in g_cached.drives

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)


@pytest.mark.asyncio()
async def test_transform():
    autd: Controller[Audit]
    with await create_controller() as autd:

        def transform(dev: Device, _tr: Transducer, d: Drive) -> Drive:
            if dev.idx == 0:
                return Drive(Phase(d.phase.value + 32), d.intensity)

            return Drive(Phase(d.phase.value - 32), d.intensity)

        assert await autd.send_async(Uniform(0x80).with_phase(Phase(128)).with_transform(transform))

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 128 + 32)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 128 - 32)


@pytest.mark.asyncio()
async def test_transform_check_only_for_enabled():
    autd: Controller[Audit]
    with await create_controller() as autd:
        autd.geometry[0].enable = False

        check = np.zeros(2, dtype=bool)

        def transform(dev: Device, _tr: Transducer, d: Drive) -> Drive:
            check[dev.idx] = True
            return d

        assert await autd.send_async(Uniform(0x80).with_phase(Phase(0x90)).with_transform(transform))

        assert not check[0]
        assert check[1]

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)


@pytest.mark.asyncio()
async def test_gain_segment():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert autd.link.current_stm_segment(0) == Segment.S0

        assert await autd.send_async(Uniform(0x01).with_phase(Phase(0x02)))
        assert autd.link.current_stm_segment(0) == Segment.S0
        assert autd.link.stm_cycle(0, Segment.S0) == 1
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0xFFFFFFFF
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x01)
            assert np.all(phases == 0x02)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x00)
            assert np.all(phases == 0x00)

        assert await autd.send_async(Uniform(0x03).with_phase(Phase(0x04)).with_segment(Segment.S1, update_segment=True))
        assert autd.link.current_stm_segment(0) == Segment.S1
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x01)
            assert np.all(phases == 0x02)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x03)
            assert np.all(phases == 0x04)

        assert await autd.send_async(Uniform(0x05).with_phase(Phase(0x06)).with_segment(Segment.S0, update_segment=False))
        assert autd.link.current_stm_segment(0) == Segment.S1
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x05)
            assert np.all(phases == 0x06)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x03)
            assert np.all(phases == 0x04)

        assert await autd.send_async(ChangeGainSegment(Segment.S0))
        assert autd.link.current_stm_segment(0) == Segment.S0
