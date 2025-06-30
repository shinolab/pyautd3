from .test_autd import create_controller


def test_environment_sound_speed():
    with create_controller() as autd:
        assert autd.environment.sound_speed == 340e3
        autd.environment.sound_speed = 350e3
        assert autd.environment.sound_speed == 350e3


def test_environment_set_sound_speed_from_temp():
    with create_controller() as autd:
        autd.environment.set_sound_speed_from_temp(15)
        assert autd.environment.sound_speed == 340.29525e3


def test_environment_wavelength():
    with create_controller() as autd:
        assert autd.environment.wavelength() == 340e3 / 40e3


def test_environment_wavenum():
    with create_controller() as autd:
        assert autd.environment.wavenumber() == 0.7391983270645142
