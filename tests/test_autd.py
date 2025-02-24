import platform

import numpy as np
import pytest

from pyautd3 import AUTD3, Clear, Controller, Device, ForceFan, Segment, tracing_init
from pyautd3.autd_error import AUTDError, InvalidDatagramTypeError
from pyautd3.controller.controller import SenderOption
from pyautd3.controller.sleeper import SpinSleeper, SpinStrategy, StdSleeper, WaitableSleeper
from pyautd3.driver.datagram import Synchronize
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.firmware_version import FirmwareInfo
from pyautd3.gain import Null, Uniform
from pyautd3.link.audit import Audit
from pyautd3.modulation import Sine, Static
from pyautd3.modulation.sine import SineOption
from pyautd3.native_methods.autd3capi import NativeMethods as Base


def create_controller() -> Controller[Audit]:
    return Controller.open(
        [AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0]), AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])],
        Audit(),
    )


def test_sender_is_default():
    assert Base().sender_option_is_default(SenderOption()._inner())


def test_sleeper():
    _ = StdSleeper(timer_resolution=1)._inner()
    _ = SpinSleeper().with_spin_strategy(SpinStrategy.SpinLoopHint)._inner()
    if platform.system() == "Windows":
        _ = WaitableSleeper()._inner()
    else:
        with pytest.raises(RuntimeError):
            _ = WaitableSleeper()._inner()


def test_firmware_info():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert FirmwareInfo.latest_version() == "v10.0.1"

        for i, firm in enumerate(autd.firmware_version()):
            assert firm.info == f"{i}: CPU = v10.0.1, FPGA = v10.0.1 [Emulator]"
            assert str(firm) == f"{i}: CPU = v10.0.1, FPGA = v10.0.1 [Emulator]"


def test_close():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link().is_open()

        autd.close()
        autd.close()

    with create_controller() as autd:
        autd.link().break_down()
        with pytest.raises(AUTDError) as e:
            autd.close()
        assert str(e.value) == "broken"


def test_send_single():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0xFF)

        autd.send(Static())

        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0xFF)

        autd.link().break_down()
        with pytest.raises(AUTDError) as e:
            autd.send(Static())
        assert str(e.value) == "broken"
        autd.link().repair()


def test_send_tuple():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0xFF)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)

        autd.send((Static(), Uniform(intensity=EmitIntensity(0x80), phase=Phase(0))))
        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0xFF)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        with pytest.raises(InvalidDatagramTypeError):
            autd.send(0)  # type: ignore[arg-type]

        autd.link().break_down()
        with pytest.raises(AUTDError) as e:
            autd.send((Static(), Uniform(intensity=EmitIntensity(0xFF), phase=Phase(0))))
        assert str(e.value) == "broken"
        autd.link().repair()


def test_group():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.group_send(
            key_map=lambda dev: dev.idx(),
            data_map={1: Null(), 0: (Sine(freq=150 * Hz, option=SineOption()), Uniform(intensity=EmitIntensity(0xFF), phase=Phase(0)))},
        )

        mod = autd.link().modulation_buffer(0, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link().drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0xFF)
        assert np.all(phases == 0)

        mod = autd.link().modulation_buffer(1, Segment.S0)
        intensities, phases = autd.link().drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0)

        with pytest.raises(InvalidDatagramTypeError):
            autd.group_send(lambda dev: dev.idx(), {0: 0})  # type: ignore[dict-item]


def test_group_check_only_for_enabled():
    autd: Controller[Audit]
    with create_controller() as autd:
        check = np.zeros(autd.num_devices(), dtype=bool)

        autd.geometry()[0].enable = False

        def key_map(dev: Device) -> int:
            check[dev.idx()] = True
            return 0

        autd.group_send(key_map, {0: (Sine(freq=150 * Hz, option=SineOption()), Uniform(intensity=EmitIntensity(0x80), phase=Phase(0x90)))})

        assert not check[0]
        assert check[1]

        mod = autd.link().modulation_buffer(0, Segment.S0)
        intensities, phases = autd.link().drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        mod = autd.link().modulation_buffer(1, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link().drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)


def test_clear():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send((Static(), Uniform(intensity=EmitIntensity(0xFF), phase=Phase(0x90))))

        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0xFF)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0x90)

        autd.send(Clear())

        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0xFF)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)


def test_synchronize():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Synchronize())


def test_force_fan():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert not autd.link().is_force_fan(dev.idx())

        autd.send(ForceFan(lambda dev: dev.idx() == 0))
        assert autd.link().is_force_fan(0)
        assert not autd.link().is_force_fan(1)

        autd.send(ForceFan(lambda dev: dev.idx() == 1))
        assert not autd.link().is_force_fan(0)
        assert autd.link().is_force_fan(1)


def test_geometry():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.num_transducers() == 249 * 2
        assert autd[0].num_transducers() == 249


def test_tracing():
    tracing_init()
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.close()
