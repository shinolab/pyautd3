import numpy as np

from pyautd3.driver.datagram.stm.control_point import (
    ControlPoint,
    ControlPoints1,
    ControlPoints2,
    ControlPoints3,
    ControlPoints4,
    ControlPoints5,
    ControlPoints6,
    ControlPoints7,
    ControlPoints8,
)
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase


def test_control_point():
    c = ControlPoint(point=[1.0, 2.0, 3.0], phase_offset=Phase(0x80))
    assert np.array_equal(c.point, [1.0, 2.0, 3.0])
    assert c.offset == Phase(0x80)


def test_control_points_1():
    c = ControlPoints1(points=[4.0, 5.0, 6.0], intensity=EmitIntensity(0x80))
    assert np.array_equal(c.points, np.array([np.array([4.0, 5.0, 6.0])]))
    assert c.intensity == EmitIntensity(0x80)


def test_control_points_2():
    c = ControlPoints2(
        points=(
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ),
        intensity=EmitIntensity(0x80),
    )
    assert np.array_equal(c.points, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
    assert c.intensity == EmitIntensity(0x80)


def test_control_points_3():
    c = ControlPoints3(
        points=(
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
        ),
        intensity=EmitIntensity(0x80),
    )
    assert np.array_equal(c.points, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]))
    assert c.intensity == EmitIntensity(0x80)


def test_control_points_4():
    c = ControlPoints4(
        points=(
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            [10.0, 11.0, 12.0],
        ),
        intensity=EmitIntensity(0x80),
    )
    assert np.array_equal(c.points, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [10.0, 11.0, 12.0]]))
    assert c.intensity == EmitIntensity(0x80)


def test_control_points_5():
    c = ControlPoints5(
        points=(
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            [10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0],
        ),
        intensity=EmitIntensity(0x80),
    )
    assert np.array_equal(c.points, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [10.0, 11.0, 12.0], [13.0, 14.0, 15.0]]))
    assert c.intensity == EmitIntensity(0x80)


def test_control_points_6():
    c = ControlPoints6(
        points=(
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            [10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0],
            [16.0, 17.0, 18.0],
        ),
        intensity=EmitIntensity(0x80),
    )
    assert np.array_equal(
        c.points,
        np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [10.0, 11.0, 12.0], [13.0, 14.0, 15.0], [16.0, 17.0, 18.0]]),
    )
    assert c.intensity == EmitIntensity(0x80)


def test_control_points_7():
    c = ControlPoints7(
        points=(
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            [10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0],
            [16.0, 17.0, 18.0],
            [19.0, 20.0, 21.0],
        ),
        intensity=EmitIntensity(0x80),
    )
    assert np.array_equal(
        c.points,
        np.array(
            [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [10.0, 11.0, 12.0], [13.0, 14.0, 15.0], [16.0, 17.0, 18.0], [19.0, 20.0, 21.0]],
        ),
    )
    assert c.intensity == EmitIntensity(0x80)


def test_control_points_8():
    c = ControlPoints8(
        points=(
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            [10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0],
            [16.0, 17.0, 18.0],
            [19.0, 20.0, 21.0],
            [22.0, 23.0, 24.0],
        ),
        intensity=EmitIntensity(0x80),
    )
    assert np.array_equal(
        c.points,
        np.array(
            [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0],
                [10.0, 11.0, 12.0],
                [13.0, 14.0, 15.0],
                [16.0, 17.0, 18.0],
                [19.0, 20.0, 21.0],
                [22.0, 23.0, 24.0],
            ],
        ),
    )
    assert c.intensity == EmitIntensity(0x80)
