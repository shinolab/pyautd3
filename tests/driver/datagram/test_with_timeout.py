from datetime import timedelta

from pyautd3.controller.controller import Controller
from pyautd3.driver.autd3_device import AUTD3
from pyautd3.gain.null import Null
from pyautd3.link.audit import Audit


def test_with_timeout():
    autd: Controller[Audit]
    with Controller.builder([AUTD3([0.0, 0.0, 0.0]), AUTD3([0.0, 0.0, 0.0])]).open(
        Audit.builder().with_timeout(timedelta(seconds=0)),
    ) as autd:
        assert autd.link.timeout() == timedelta(seconds=0)
        assert autd.link.last_timeout() == timedelta(milliseconds=200)

        autd.send(Null())
        assert autd.link.last_timeout() is None

        autd.send(Null().with_timeout(timedelta(milliseconds=100)))
        assert autd.link.last_timeout() == timedelta(milliseconds=100)

        autd.send((Null(), Null()).with_timeout(timedelta(milliseconds=200)))  # type: ignore[attr-defined]
        assert autd.link.last_timeout() == timedelta(milliseconds=200)
