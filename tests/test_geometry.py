import numpy as np
import pytest
from numpy.typing import ArrayLike

from pyautd3 import AUTD3, Controller, EulerAngles, deg, rad
from pyautd3.driver.geometry.rotation import Angle
from pyautd3.link.audit import Audit

from .test_autd import create_controller


def test_angle():
    assert (np.pi / 2 * rad).radian == np.pi / 2
    assert (90 * deg).radian == np.pi / 2


def test_angle_ctr():
    with pytest.raises(NotImplementedError):
        _ = Angle()

    with pytest.raises(NotImplementedError):
        _ = Angle._UnitDegree()

    with pytest.raises(NotImplementedError):
        _ = Angle._UnitRad()

    with pytest.raises(NotImplementedError):
        _ = EulerAngles()


def test_with_rotation_xyz():
    def open_with_rotation(q: ArrayLike) -> Controller[Audit]:
        return Controller.builder([AUTD3([0.0, 0.0, 0.0]).with_rotation(q)]).open(Audit.builder())

    with open_with_rotation(EulerAngles.XYZ(90 * deg, 0 * deg, 0 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [1.0, 0.0, 0.0])
        assert np.allclose(autd.geometry[0].y_direction, [0.0, 0.0, 1.0])
        assert np.allclose(autd.geometry[0].axial_direction, [0.0, -1.0, 0.0])

    with open_with_rotation(EulerAngles.XYZ(0 * deg, 90 * deg, 0 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 0.0, -1.0])
        assert np.allclose(autd.geometry[0].y_direction, [0.0, 1.0, 0.0])
        assert np.allclose(autd.geometry[0].axial_direction, [1.0, 0.0, 0.0])

    with open_with_rotation(EulerAngles.XYZ(0 * deg, 0 * deg, 90 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 1.0, 0.0])
        assert np.allclose(autd.geometry[0].y_direction, [-1.0, 0.0, 0.0])
        assert np.allclose(autd.geometry[0].axial_direction, [0.0, 0.0, 1.0])

    with open_with_rotation(EulerAngles.XYZ(0 * deg, 90 * deg, 90 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 1.0, 0.0])
        assert np.allclose(autd.geometry[0].y_direction, [0.0, 0.0, 1.0])
        assert np.allclose(autd.geometry[0].axial_direction, [1.0, 0.0, 0.0])

    with open_with_rotation(EulerAngles.XYZ(90 * deg, 90 * deg, 0 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 1.0, 0.0])
        assert np.allclose(autd.geometry[0].y_direction, [0.0, 0.0, 1.0])
        assert np.allclose(autd.geometry[0].axial_direction, [1.0, 0.0, 0.0])


def test_with_rotation_zyz():
    def open_with_rotation(q: ArrayLike) -> Controller[Audit]:
        return Controller.builder([AUTD3([0.0, 0.0, 0.0]).with_rotation(q)]).open(Audit.builder())

    with open_with_rotation(EulerAngles.ZYZ(90 * deg, 0 * deg, 0 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 1.0, 0.0])
        assert np.allclose(autd.geometry[0].y_direction, [-1.0, 0.0, 0.0])
        assert np.allclose(autd.geometry[0].axial_direction, [0.0, 0.0, 1.0])

    with open_with_rotation(EulerAngles.ZYZ(0 * deg, 90 * deg, 0 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 0.0, -1.0])
        assert np.allclose(autd.geometry[0].y_direction, [0.0, 1.0, 0.0])
        assert np.allclose(autd.geometry[0].axial_direction, [1.0, 0.0, 0.0])

    with open_with_rotation(EulerAngles.ZYZ(0 * deg, 0 * deg, 90 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 1.0, 0.0])
        assert np.allclose(autd.geometry[0].y_direction, [-1.0, 0.0, 0.0])
        assert np.allclose(autd.geometry[0].axial_direction, [0.0, 0.0, 1.0])

    with open_with_rotation(EulerAngles.ZYZ(0 * deg, 90 * deg, 90 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 1.0, 0.0])
        assert np.allclose(autd.geometry[0].y_direction, [0.0, 0.0, 1.0])
        assert np.allclose(autd.geometry[0].axial_direction, [1.0, 0.0, 0.0])

    with open_with_rotation(EulerAngles.ZYZ(90 * deg, 90 * deg, 0 * deg)) as autd:
        assert np.allclose(autd.geometry[0].x_direction, [0.0, 0.0, -1.0])
        assert np.allclose(autd.geometry[0].y_direction, [-1.0, 0.0, 0.0])
        assert np.allclose(autd.geometry[0].axial_direction, [0.0, 1.0, 0.0])


def test_geometry_num_devices():
    with create_controller() as autd:
        assert autd.geometry.num_devices == 2


def test_geometry_center():
    with create_controller() as autd:
        center = autd.geometry.center
        assert len(center) == 3
        assert center[0] == 86.625267028808594
        assert center[1] == 66.71319580078125
        assert center[2] == 0.0


def test_device_idx():
    with create_controller() as autd:
        assert autd.geometry[0].idx == 0
        assert autd.geometry[1].idx == 1


def test_device_sound_speed():
    with create_controller() as autd:
        for dev in autd.geometry:
            assert dev.sound_speed == 340e3
            dev.sound_speed = 350e3
            assert dev.sound_speed == 350e3


def test_device_set_sound_speed_from_temp():
    with create_controller() as autd:
        for dev in autd.geometry:
            dev.set_sound_speed_from_temp(15)
            assert dev.sound_speed == 340.29525e3

        autd.geometry.set_sound_speed(350e3)
        for dev in autd.geometry:
            assert dev.sound_speed == 350e3

        autd.geometry.set_sound_speed_from_temp(15)
        for dev in autd.geometry:
            assert dev.sound_speed == 340.29525e3


def test_device_enable():
    with create_controller() as autd:
        for dev in autd.geometry:
            assert dev.enable
            dev.enable = False
            assert not dev.enable


def test_device_num_transducers():
    with create_controller() as autd:
        assert autd.geometry.num_transducers == 249 * autd.geometry.num_devices
        for dev in autd.geometry:
            assert dev.num_transducers == 249


def test_device_center():
    with create_controller() as autd:
        for dev in autd.geometry:
            center = dev.center
            assert len(center) == 3
            assert center[0] == 86.625267028808594
            assert center[1] == 66.71319580078125
            assert center[2] == 0.0


def test_device_translate():
    with create_controller() as autd:
        for dev in autd.geometry:
            original_pos = [tr.position for tr in dev]
            t = [1, 2, 3]
            dev.translate(t)
            for tr in dev:
                assert np.allclose(tr.position, original_pos[tr.idx] + t)


def test_device_rotate():
    with create_controller() as autd:
        for dev in autd.geometry:
            r = [0.70710678, 0.0, 0.0, 0.70710678]
            dev.rotate(r)
            assert np.allclose(dev.rotation, r)


def test_device_affine():
    with create_controller() as autd:
        for dev in autd.geometry:
            original_pos = [tr.position for tr in dev]
            t = [1, 2, 3]
            r = [0.70710678, 0.0, 0.0, 0.70710678]
            dev.affine(t, r)
            for tr in dev:
                op = original_pos[tr.idx]
                expected = np.array([-op[1], op[0], op[2]]) + t
                assert np.allclose(tr.position, expected)
            assert np.allclose(dev.rotation, r)


def test_device_wavelength():
    with create_controller() as autd:
        for dev in autd.geometry:
            assert dev.wavelength == 340e3 / 40e3


def test_device_wavenum():
    with create_controller() as autd:
        for dev in autd.geometry:
            assert dev.wavenumber == 0.7391983270645142


def test_transducer_idx():
    with create_controller() as autd:
        for dev in autd.geometry:
            for i, tr in enumerate(dev):
                assert tr.idx == i


def test_transducer_dev_idx():
    with create_controller() as autd:
        for dev in autd.geometry:
            for tr in dev:
                assert tr.dev_idx == dev.idx


def test_transducer_position():
    with create_controller() as autd:
        assert np.allclose(autd.geometry[0][0].position, [0.0, 0.0, 0.0])
        assert np.allclose(
            autd.geometry[0][-1].position,
            [(AUTD3.NUM_TRANS_IN_X - 1) * AUTD3.TRANS_SPACING, (AUTD3.NUM_TRANS_IN_Y - 1) * AUTD3.TRANS_SPACING, 0.0],
        )

        assert np.allclose(autd.geometry[1][0].position, [0.0, 0.0, 0.0])
        assert np.allclose(
            autd.geometry[1][-1].position,
            [(AUTD3.NUM_TRANS_IN_X - 1) * AUTD3.TRANS_SPACING, (AUTD3.NUM_TRANS_IN_Y - 1) * AUTD3.TRANS_SPACING, 0.0],
        )


def test_transducer_rotation():
    with create_controller() as autd:
        for dev in autd.geometry:
            assert np.allclose(dev.rotation, [1.0, 0.0, 0.0, 0.0])


def test_transducer_x_direction():
    with create_controller() as autd:
        for dev in autd.geometry:
            assert np.allclose(dev.x_direction, [1.0, 0.0, 0.0])


def test_transducer_y_direction():
    with create_controller() as autd:
        for dev in autd.geometry:
            assert np.allclose(dev.y_direction, [0.0, 1.0, 0.0])


def test_transducer_axial_direction():
    with create_controller() as autd:
        for dev in autd.geometry:
            assert np.allclose(dev.axial_direction, [0.0, 0.0, 1.0])
