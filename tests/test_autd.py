import numpy as np
import pytest

from pyautd3 import AUTD3, Clear, Controller, ForceFan, Segment
from pyautd3.autd_error import AUTDError, InvalidDatagramTypeError
from pyautd3.controller import FixedDelay, FixedSchedule
from pyautd3.controller.controller import SenderOption
from pyautd3.controller.sleeper import SpinSleeper, SpinStrategy, SpinWaitSleeper, StdSleeper
from pyautd3.driver.datagram import Synchronize
from pyautd3.driver.firmware.fpga.emit_intensity import Intensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.firmware_version import FirmwareInfo
from pyautd3.gain import Uniform
from pyautd3.link.audit import Audit
from pyautd3.modulation import Static
from pyautd3.native_methods.autd3 import ParallelMode
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.utils.duration import Duration


def create_controller() -> Controller[Audit]:
    return Controller.open(
        [AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0]), AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])],
        Audit(),
    )


def test_sender_is_default():
    assert Base().sender_option_is_default(SenderOption()._inner())


def test_sleeper():
    _ = StdSleeper()._inner()
    _ = SpinSleeper().with_spin_strategy(SpinStrategy.SpinLoopHint)._inner()
    _ = SpinWaitSleeper()._inner()


def test_firmware_info():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert FirmwareInfo.latest_version() == "v12.1.0"

        for i, firm in enumerate(autd.firmware_version()):
            assert firm.info == f"{i}: CPU = v12.1.0, FPGA = v12.1.0 [Emulator]"
            assert str(firm) == f"{i}: CPU = v12.1.0, FPGA = v12.1.0 [Emulator]"


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


def test_sender():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0xFF)

        autd.sender(SenderOption(), FixedSchedule(StdSleeper())).send(Static(intensity=0x80))
        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0x80)

        autd.sender(SenderOption(), FixedDelay(SpinWaitSleeper())).send(Static(intensity=0x81))
        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0x81)


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

        autd.send((Static(), Uniform(intensity=Intensity(0x80), phase=Phase(0))))
        for dev in autd.geometry():
            assert np.all(autd.link().modulation_buffer(dev.idx(), Segment.S0) == 0xFF)
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        with pytest.raises(InvalidDatagramTypeError):
            autd.send(0)  # type: ignore[arg-type]

        autd.link().break_down()
        with pytest.raises(AUTDError) as e:
            autd.send((Static(), Uniform(intensity=Intensity(0xFF), phase=Phase(0))))
        assert str(e.value) == "broken"
        autd.link().repair()


def test_clear():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send((Static(), Uniform(intensity=Intensity(0xFF), phase=Phase(0x90))))

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


def test_sender_option():
    autd: Controller[Audit]
    with create_controller() as autd:
        option = SenderOption(
            send_interval=Duration.from_millis(1),
            receive_interval=Duration.from_millis(1),
            timeout=Duration.from_millis(100),
            parallel=ParallelMode.Off,
        )
        autd.default_sender_option = option
        assert option == autd.default_sender_option
