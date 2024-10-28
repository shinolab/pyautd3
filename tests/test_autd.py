from datetime import timedelta

import numpy as np
import pytest

from pyautd3 import AUTD3, Clear, Controller, Device, ForceFan, Segment, tracing_init
from pyautd3.autd_error import AUTDError, InvalidDatagramTypeError, KeyAlreadyExistsError
from pyautd3.controller.timer import AsyncSleeper, SpinSleeper, StdSleeper, TimerStrategy, WaitableSleeper
from pyautd3.driver.datagram import Synchronize
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.firmware_version import FirmwareInfo
from pyautd3.gain import Null, Uniform
from pyautd3.link.audit import Audit
from pyautd3.modulation import Sine, Static
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import SpinStrategyTag


async def create_controller_async() -> Controller[Audit]:
    return (
        await Controller.builder([AUTD3([0.0, 0.0, 0.0]), AUTD3([0.0, 0.0, 0.0])])
        .with_send_interval(timedelta(milliseconds=1))
        .with_receive_interval(timedelta(milliseconds=1))
        .with_fallback_parallel_threshold(4)
        .with_fallback_timeout(timedelta(milliseconds=20))
        .with_timer_strategy(TimerStrategy.Spin(SpinSleeper()))
        .open_async(
            Audit.builder(),
        )
    )


def create_controller() -> Controller[Audit]:
    return (
        Controller.builder([AUTD3([0.0, 0.0, 0.0]), AUTD3([0.0, 0.0, 0.0])])
        .with_send_interval(timedelta(milliseconds=1))
        .with_receive_interval(timedelta(milliseconds=1))
        .with_fallback_parallel_threshold(4)
        .with_fallback_timeout(timedelta(milliseconds=20))
        .with_timer_strategy(TimerStrategy.Spin(SpinSleeper()))
        .open(Audit.builder())
    )


def test_controller_is_default():
    default = Controller.builder([])
    assert Base().controller_builder_is_default(
        default.fallback_parallel_threshold,
        int(default.fallback_timeout.total_seconds() * 1000 * 1000 * 1000),
        int(default.send_interval.total_seconds() * 1000 * 1000 * 1000),
        int(default.receive_interval.total_seconds() * 1000 * 1000 * 1000),
        default.timer_strategy,
    )


def test_with_timer():
    autd: Controller[Audit]
    with Controller.builder([]).with_timer_strategy(TimerStrategy.Std(StdSleeper())).open(Audit.builder()) as autd:
        autd.send(Static())
    with (
        Controller.builder([])
        .with_timer_strategy(
            TimerStrategy.Spin(SpinSleeper(700_000).with_spin_strategy(SpinStrategyTag.SpinLoopHint)),
        )
        .open(Audit.builder()) as autd
    ):
        autd.send(Static())
    with Controller.builder([]).with_timer_strategy(TimerStrategy.Async(AsyncSleeper())).open(Audit.builder()) as autd:
        autd.send(Static())

    _ = TimerStrategy.Waitable(WaitableSleeper())

    with pytest.raises(NotImplementedError):
        _ = TimerStrategy()


def test_firmware_info():
    autd: Controller[Audit]
    with create_controller() as autd:
        for i, firm in enumerate(autd.firmware_version()):
            assert firm.info == f"{i}: CPU = v10.0.1, FPGA = v10.0.1 [Emulator]"
            assert str(firm) == f"{i}: CPU = v10.0.1, FPGA = v10.0.1 [Emulator]"

        autd.link.down()
        with pytest.raises(AUTDError) as e:
            autd.firmware_version()
        assert str(e.value) == "Read firmware info failed: 0, 1"
        autd.link.up()


@pytest.mark.asyncio
async def test_firmware_info_async():
    autd: Controller[Audit]
    with await create_controller_async() as autd:
        assert FirmwareInfo.latest_version() == "v10.0.1"

        for i, firm in enumerate(await autd.firmware_version_async()):
            assert firm.info == f"{i}: CPU = v10.0.1, FPGA = v10.0.1 [Emulator]"
            assert str(firm) == f"{i}: CPU = v10.0.1, FPGA = v10.0.1 [Emulator]"

        autd.link.down()
        with pytest.raises(AUTDError) as e:
            await autd.firmware_version_async()
        assert str(e.value) == "Read firmware info failed: 0, 1"
        autd.link.up()


def test_close():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link.is_open()

        autd.close()
        autd.close()

    with create_controller() as autd:
        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            autd.close()
        assert str(e.value) == "broken"


@pytest.mark.asyncio
async def test_close_async():
    autd: Controller[Audit]
    with await create_controller_async() as autd:
        assert autd.link.is_open()

        await autd.close_async()
        await autd.close_async()

    with create_controller() as autd:
        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            await autd.close_async()
        assert str(e.value) == "broken"


def test_send_single():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)

        autd.send(Static())

        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)

        autd.link.down()
        with pytest.raises(AUTDError) as e:
            autd.send(Static())
        assert str(e.value) == "Failed to send data"
        autd.link.up()

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            autd.send(Static())
        assert str(e.value) == "broken"
        autd.link.repair()


@pytest.mark.asyncio
async def test_send_async_single():
    autd: Controller[Audit]
    with await create_controller_async() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)

        await autd.send_async(Static())

        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)

        autd.link.down()
        with pytest.raises(AUTDError) as e:
            await autd.send_async(Static())
        assert str(e.value) == "Failed to send data"
        autd.link.up()

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            await autd.send_async(Static())
        assert str(e.value) == "broken"
        autd.link.repair()


@pytest.mark.asyncio
async def test_send_async_tuple():
    autd: Controller[Audit]
    with await create_controller_async() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)

        await autd.send_async((Static(), Uniform(EmitIntensity(0x80))))
        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        with pytest.raises(InvalidDatagramTypeError):
            await autd.send_async(0)  # type: ignore[arg-type]

        autd.link.down()
        with pytest.raises(AUTDError) as e:
            await autd.send_async((Static(), Uniform(EmitIntensity(0xFF))))
        assert str(e.value) == "Failed to send data"
        autd.link.up()

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            await autd.send_async((Static(), Uniform(EmitIntensity(0xFF))))
        assert str(e.value) == "broken"
        autd.link.repair()


def test_send_tuple():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)

        autd.send((Static(), Uniform(EmitIntensity(0x80))))
        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        with pytest.raises(InvalidDatagramTypeError):
            autd.send(0)  # type: ignore[arg-type]

        autd.link.down()
        with pytest.raises(AUTDError) as e:
            autd.send((Static(), Uniform(EmitIntensity(0xFF))))
        assert str(e.value) == "Failed to send data"
        autd.link.up()

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            autd.send((Static(), Uniform(EmitIntensity(0xFF))))
        assert str(e.value) == "broken"
        autd.link.repair()


@pytest.mark.asyncio
async def test_group_async():
    autd: Controller[Audit]
    with await create_controller_async() as autd:
        await autd.group(lambda dev: dev.idx).set(1, Null()).set(0, (Sine(150 * Hz), Uniform(EmitIntensity(0xFF)))).send_async()

        mod = autd.link.modulation_buffer(0, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link.drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0xFF)
        assert np.all(phases == 0)

        mod = autd.link.modulation_buffer(1, Segment.S0)
        intensities, phases = autd.link.drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0)

        with pytest.raises(InvalidDatagramTypeError):
            await autd.group(lambda dev: dev.idx).set(0, 0).send_async()  # type: ignore[arg-type]

        with pytest.raises(KeyAlreadyExistsError):
            await autd.group(lambda dev: dev.idx).set(0, Null()).set(0, Null()).send_async()


def test_group():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.group(lambda dev: dev.idx).set(1, Null()).set(0, (Sine(150 * Hz), Uniform(EmitIntensity(0xFF)))).send()

        mod = autd.link.modulation_buffer(0, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link.drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0xFF)
        assert np.all(phases == 0)

        mod = autd.link.modulation_buffer(1, Segment.S0)
        intensities, phases = autd.link.drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0)

        with pytest.raises(InvalidDatagramTypeError):
            autd.group(lambda dev: dev.idx).set(0, 0).send()  # type: ignore[arg-type]

        with pytest.raises(KeyAlreadyExistsError):
            autd.group(lambda dev: dev.idx).set(0, Null()).set(0, Null()).send()


def test_group_check_only_for_enabled():
    autd: Controller[Audit]
    with create_controller() as autd:
        check = np.zeros(autd.num_devices, dtype=bool)

        autd.geometry[0].enable = False

        def f(dev: Device) -> int:
            check[dev.idx] = True
            return 0

        autd.group(f).set(0, (Sine(150 * Hz), Uniform((EmitIntensity(0x80), Phase(0x90))))).send()

        assert not check[0]
        assert check[1]

        mod = autd.link.modulation_buffer(0, Segment.S0)
        intensities, phases = autd.link.drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        mod = autd.link.modulation_buffer(1, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link.drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)


def test_clear():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send((Static(), Uniform((EmitIntensity(0xFF), Phase(0x90)))))

        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0x90)

        autd.send(Clear())

        for dev in autd.geometry:
            assert np.all(autd.link.modulation_buffer(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)


def test_synchronize():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Synchronize())


def test_force_fan():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert not autd.link.is_force_fan(dev.idx)

        autd.send(ForceFan(lambda dev: dev.idx == 0))
        assert autd.link.is_force_fan(0)
        assert not autd.link.is_force_fan(1)

        autd.send(ForceFan(lambda dev: dev.idx == 1))
        assert not autd.link.is_force_fan(0)
        assert autd.link.is_force_fan(1)


def test_geometry():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.num_transducers == 249 * 2
        assert autd[0].num_transducers == 249


def test_tracing():
    tracing_init()
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.close()
