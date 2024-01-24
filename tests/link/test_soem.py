import ctypes
import os
from datetime import timedelta

import pytest

from pyautd3 import AUTD3, Controller, TimerStrategy
from pyautd3.autd_error import AUTDError
from pyautd3.link.soem import SOEM, OnErrFunc, RemoteSOEM, SyncMode


@pytest.mark.soem()
def test_soem_adapers():
    adapters = SOEM.enumerate_adapters()
    for adapter in adapters:
        print(adapter)


def on_lost_f(msg: ctypes.c_char_p):
    if msg.value is not None:
        print(msg.value.decode("utf-8"), end="")
    os._exit(-1)


def on_err_f(msg: ctypes.c_char_p):
    if msg.value is not None:
        print(msg.value.decode("utf-8"), end="")


@pytest.mark.soem()
def test_soem():
    on_lost = OnErrFunc(on_lost_f)
    on_err = OnErrFunc(on_err_f)
    with pytest.raises(AUTDError) as _, (
        Controller.builder()
        .add_device(AUTD3([0.0, 0.0, 0.0]))
        .open_with(
            SOEM.builder()
            .with_ifname("")
            .with_buf_size(32)
            .with_send_cycle(2)
            .with_sync0_cycle(2)
            .with_on_lost(on_lost)
            .with_on_err(on_err)
            .with_timer_strategy(TimerStrategy.Sleep)
            .with_sync_mode(SyncMode.FreeRun)
            .with_state_check_interval(timedelta(milliseconds=100))
            .with_timeout(timedelta(milliseconds=200)),
        )
    ) as _:
        pass


@pytest.mark.soem()
def test_remote_soem():
    _ = RemoteSOEM.builder("127.0.0.1:8080").with_timeout(timedelta(milliseconds=200))
