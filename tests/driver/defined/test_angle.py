from pyautd3.driver.common import rad


def test_angle():
    assert 1.0 * rad == 1.0 * rad
    assert 1.0 * rad != 2.0 * rad
    assert 1.0 * rad != 2.0
