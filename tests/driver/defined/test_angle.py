from pyautd3.driver.defined import rad


def test_angle():
    assert 1.0 * rad == 1.0 * rad
    assert 1.0 * rad != 2.0 * rad
    assert 1.0 * rad != 2.0
