import numpy as np
import pytest

from pyautd3 import (
    AUTD3,
    Clear,
    ConfigureDebugOutputIdx,
    ConfigureForceFan,
    ConfigureSilencer,
    Controller,
    Device,
    GainSTM,
    Phase,
    SamplingConfiguration,
    Segment,
)
from pyautd3.autd_error import AUTDError, InvalidDatagramTypeError, KeyAlreadyExistsError
from pyautd3.driver.datagram import Synchronize
from pyautd3.driver.firmware_version import FirmwareInfo
from pyautd3.gain import Null, Uniform
from pyautd3.link.audit import Audit
from pyautd3.modulation import Sine, Static


async def create_controller() -> Controller[Audit]:
    return await (
        Controller.builder()
        .add_device(AUTD3([0.0, 0.0, 0.0]))
        .add_device(AUTD3([0.0, 0.0, 0.0]))
        .open_async(
            Audit.builder(),
        )
    )


def create_controller_sync() -> Controller[Audit]:
    return (
        Controller.builder()
        .add_device(AUTD3([0.0, 0.0, 0.0]))
        .add_device(AUTD3([0.0, 0.0, 0.0]))
        .open(
            Audit.builder(),
        )
    )


@pytest.mark.asyncio()
async def test_silencer_fixed_completion_steps():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        await autd.send_async(ConfigureSilencer.fixed_completion_steps(2, 3))

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 2
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 3
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        await autd.send_async(ConfigureSilencer.disable())

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 1
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 1
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        await autd.send_async(ConfigureSilencer.default())

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)


@pytest.mark.asyncio()
async def test_silencer_fixed_update_rate():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        await autd.send_async(ConfigureSilencer.fixed_update_rate(2, 3))

        for dev in autd.geometry:
            assert autd.link.silencer_update_rate_intensity(dev.idx) == 2
            assert autd.link.silencer_update_rate_phase(dev.idx) == 3
            assert not autd.link.silencer_fixed_completion_steps_mode(dev.idx)


@pytest.mark.asyncio()
async def test_silencer_large_steps():
    autd: Controller[Audit]
    with await create_controller() as autd:
        await autd.send_async(ConfigureSilencer.disable())
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 1
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 1
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        assert await autd.send_async(Sine(150).with_sampling_config(SamplingConfiguration.from_frequency_division(512)))

        with pytest.raises(AUTDError) as e:
            await autd.send_async(ConfigureSilencer.fixed_completion_steps(10, 40))
        assert str(e.value) == "Completion steps is too large"


@pytest.mark.asyncio()
async def test_silencer_small_freq_div_mod():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        with pytest.raises(AUTDError) as e:
            await autd.send_async(Sine(150).with_sampling_config(SamplingConfiguration.from_frequency_division(512)))
        assert str(e.value) == "Frequency division is too small"

        await autd.send_async(ConfigureSilencer.fixed_completion_steps(10, 40).with_strict_mode(mode=False))
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        assert await autd.send_async(Sine(150).with_sampling_config(SamplingConfiguration.from_frequency_division(512)))


@pytest.mark.asyncio()
async def test_silencer_small_freq_div_stm():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        with pytest.raises(AUTDError) as e:
            await autd.send_async(GainSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(512)).add_gain(Null()).add_gain(Null()))
        assert str(e.value) == "Frequency division is too small"

        await autd.send_async(ConfigureSilencer.fixed_completion_steps(10, 40).with_strict_mode(mode=False))
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        assert await autd.send_async(
            GainSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(512)).add_gain(Null()).add_gain(Null()),
        )


@pytest.mark.asyncio()
async def test_debug_output_idx():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.debug_output_idx(dev.idx) == 0xFF

        await autd.send_async(ConfigureDebugOutputIdx(lambda dev: dev[0]))

        for dev in autd.geometry:
            assert autd.link.debug_output_idx(dev.idx) == 0

        await autd.send_async(ConfigureDebugOutputIdx(lambda dev: dev[10] if dev.idx == 0 else None))

        assert autd.link.debug_output_idx(0) == 10
        assert autd.link.debug_output_idx(1) == 0xFF


def test_firmware_info():
    autd: Controller[Audit]
    with create_controller_sync() as autd:
        for i, firm in enumerate(autd.firmware_info_list()):
            assert firm.info == f"{i}: CPU = v6.0.0, FPGA = v6.0.0 [Emulator]"
            assert str(firm) == f"{i}: CPU = v6.0.0, FPGA = v6.0.0 [Emulator]"

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            autd.firmware_info_list()
        assert str(e.value) == "broken"


@pytest.mark.asyncio()
async def test_firmware_info_async():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert FirmwareInfo.latest_version() == "v6.0.0"

        for i, firm in enumerate(await autd.firmware_info_list_async()):
            assert firm.info == f"{i}: CPU = v6.0.0, FPGA = v6.0.0 [Emulator]"
            assert str(firm) == f"{i}: CPU = v6.0.0, FPGA = v6.0.0 [Emulator]"

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            await autd.firmware_info_list_async()
        assert str(e.value) == "broken"


def test_close():
    autd: Controller[Audit]
    with create_controller_sync() as autd:
        assert autd.link.is_open()

        autd.close()

        assert not autd.link.is_open()

    with create_controller_sync() as autd:
        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            autd.close()
        assert str(e.value) == "broken"


@pytest.mark.asyncio()
async def test_close_async():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert autd.link.is_open()

        await autd.close_async()

        assert not autd.link.is_open()

    with await create_controller() as autd:
        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            await autd.close_async()
        assert str(e.value) == "broken"


@pytest.mark.asyncio()
async def test_send_async_single():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)

        assert await autd.send_async(Static())

        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)

        autd.link.down()
        assert not await autd.send_async(Static())

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            await autd.send_async(Static())
        assert str(e.value) == "broken"


def test_send_single():
    autd: Controller[Audit]
    with create_controller_sync() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)

        assert autd.send(Static())

        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)

        autd.link.down()
        assert not autd.send(Static())

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            autd.send(Static())
        assert str(e.value) == "broken"


@pytest.mark.asyncio()
async def test_send_async_double():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)

        assert await autd.send_async((Static(), Uniform(0xFF)))
        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        assert await autd.send_async(Static(), Uniform(0x80))
        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        with pytest.raises(InvalidDatagramTypeError):
            await autd.send_async(0)  # type: ignore[arg-type]

        autd.link.down()
        assert not await autd.send_async((Static(), Uniform(0xFF)))

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            await autd.send_async((Static(), Uniform(0xFF)))
        assert str(e.value) == "broken"


def test_send_double():
    autd: Controller[Audit]
    with create_controller_sync() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)

        assert autd.send((Static(), Uniform(0xFF)))
        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        assert autd.send(Static(), Uniform(0x80))
        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        with pytest.raises(InvalidDatagramTypeError):
            autd.send(0)  # type: ignore[arg-type]

        autd.link.down()
        assert not autd.send((Static(), Uniform(0xFF)))

        autd.link.break_down()
        with pytest.raises(AUTDError) as e:
            autd.send((Static(), Uniform(0xFF)))
        assert str(e.value) == "broken"


@pytest.mark.asyncio()
async def test_group_async():
    autd: Controller[Audit]
    with await create_controller() as autd:
        await autd.group(lambda dev: dev.idx).set_data(0, Null()).set_data(1, Sine(150), Uniform(0xFF)).send_async()

        mod = autd.link.modulation(0, Segment.S0)
        assert len(mod) == 2
        assert np.all(mod == 0xFF)
        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        mod = autd.link.modulation(1, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0xFF)
        assert np.all(phases == 0)

        await autd.group(lambda dev: dev.idx).set_data(1, Null()).set_data(0, (Sine(150), Uniform(0xFF))).send_async()

        mod = autd.link.modulation(0, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0xFF)
        assert np.all(phases == 0)

        mod = autd.link.modulation(1, Segment.S0)
        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0)

        with pytest.raises(InvalidDatagramTypeError):
            await autd.group(lambda dev: dev.idx).set_data(0, 0).send_async()  # type: ignore[arg-type]

        with pytest.raises(KeyAlreadyExistsError):
            await autd.group(lambda dev: dev.idx).set_data(0, Null()).set_data(0, Null()).send_async()


def test_group():
    autd: Controller[Audit]
    with create_controller_sync() as autd:
        autd.group(lambda dev: dev.idx).set_data(0, Null()).set_data(1, Sine(150), Uniform(0xFF)).send()

        mod = autd.link.modulation(0, Segment.S0)
        assert len(mod) == 2
        assert np.all(mod == 0xFF)
        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        mod = autd.link.modulation(1, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0xFF)
        assert np.all(phases == 0)

        autd.group(lambda dev: dev.idx).set_data(1, Null()).set_data(0, (Sine(150), Uniform(0xFF))).send()

        mod = autd.link.modulation(0, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0xFF)
        assert np.all(phases == 0)

        mod = autd.link.modulation(1, Segment.S0)
        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0)

        with pytest.raises(InvalidDatagramTypeError):
            autd.group(lambda dev: dev.idx).set_data(0, 0).send()  # type: ignore[arg-type]

        with pytest.raises(KeyAlreadyExistsError):
            autd.group(lambda dev: dev.idx).set_data(0, Null()).set_data(0, Null()).send()


@pytest.mark.asyncio()
async def test_group_check_only_for_enabled():
    autd: Controller[Audit]
    with await create_controller() as autd:
        autd.geometry[0].enable = False

        check = np.zeros(autd.geometry.num_devices, dtype=bool)

        def f(dev: Device) -> int:
            check[dev.idx] = True
            return 0

        await autd.group(f).set_data(0, Sine(150), Uniform(0x80).with_phase(Phase(0x90))).send_async()

        assert not check[0]
        assert check[1]

        mod = autd.link.modulation(0, Segment.S0)
        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        mod = autd.link.modulation(1, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)


@pytest.mark.asyncio()
async def test_clear():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert await autd.send_async((Static(), Uniform(0xFF).with_phase(Phase(0x90))))

        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0x90)

        await autd.send_async(Clear())

        for dev in autd.geometry:
            assert np.all(autd.link.modulation(dev.idx, Segment.S0) == 0xFF)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)


@pytest.mark.asyncio()
async def test_synchronize():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert await autd.send_async(Synchronize())


@pytest.mark.asyncio()
async def test_configure_force_fan():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert not autd.link.is_force_fan(dev.idx)

        await autd.send_async(ConfigureForceFan(lambda dev: dev.idx == 0))
        assert autd.link.is_force_fan(0)
        assert not autd.link.is_force_fan(1)

        await autd.send_async(ConfigureForceFan(lambda dev: dev.idx == 1))
        assert not autd.link.is_force_fan(0)
        assert autd.link.is_force_fan(1)
