from datetime import timedelta

from pyautd3 import AUTD3, Controller
from pyautd3.link.audit import Audit


def test_audit():
    timeout = timedelta(seconds=1)
    autd: Controller[Audit]
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder().with_timeout(timeout)) as autd:
        assert autd.link.timeout() == timeout
