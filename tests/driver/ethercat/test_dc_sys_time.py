from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.utils import Duration


def test_dc_sys_time():
    now = DcSysTime(10000)
    assert now.sys_time() == 10000

    add_1 = now + Duration.from_micros(1)
    assert add_1.sys_time() == now.sys_time() + 1000

    sub_1 = now - Duration.from_micros(1)
    assert sub_1.sys_time() == now.sys_time() - 1000
