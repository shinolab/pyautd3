from pyautd3.controller.controller import Controller
from pyautd3.driver.autd3_device import AUTD3
from pyautd3.gain.null import Null
from pyautd3.link.audit import Audit
from pyautd3.utils import Duration


def test_with_timeout():
    autd: Controller[Audit]
    with Controller.builder([AUTD3([0.0, 0.0, 0.0]), AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder()) as autd:
        autd.send(Null().with_timeout(None))
        assert autd.link.last_timeout() is None

        autd.send(Null().with_timeout(Duration.from_millis(100)))
        assert autd.link.last_timeout() == Duration.from_millis(100)

        autd.send((Null(), Null()).with_timeout(Duration.from_millis(200)))  # type: ignore[attr-defined]
        assert autd.link.last_timeout() == Duration.from_millis(200)
