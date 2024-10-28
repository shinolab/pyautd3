from datetime import timedelta

import numpy as np
import pytest

from pyautd3 import AUTD3, Controller
from pyautd3.autd_error import AUTDError
from pyautd3.controller.timer import SpinSleeper, TimerStrategy
from pyautd3.driver.datagram.silencer import FixedCompletionTime, Silencer
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.emulator import Emulator, Range, Recorder, RecordOption
from pyautd3.gain import Uniform


def create_emulator() -> Emulator:
    return (
        Controller.builder([AUTD3([0.0, 0.0, 0.0]), AUTD3([0.0, 0.0, 0.0])])
        .with_send_interval(timedelta(milliseconds=1))
        .with_receive_interval(timedelta(milliseconds=1))
        .with_fallback_parallel_threshold(4)
        .with_fallback_timeout(timedelta(milliseconds=20))
        .with_timer_strategy(TimerStrategy.Spin(SpinSleeper()))
        .into_emulator()
    )


def test_record_drive():
    with create_emulator() as emulator:

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer(FixedCompletionTime(intensity=timedelta(microseconds=50), phase=timedelta(microseconds=50))))
            autd.send(Uniform((EmitIntensity(0xFF), Phase(0x40))))
            autd.tick(timedelta(microseconds=50))
            return autd

        record = emulator.record(f)

        drive = record.drive()

        assert np.array_equal(np.array([0, 25000], np.uint64), drive["time[ns]"])
        for dev in emulator.geometry:
            for tr in dev:
                assert np.array_equal(np.array([42, 128], np.uint8), drive[f"pulsewidth_{dev.idx}_{tr.idx}"])
        for dev in emulator.geometry:
            for tr in dev:
                assert np.array_equal(np.array([32, 64], np.uint8), drive[f"phase_{dev.idx}_{tr.idx}"])


@pytest.mark.asyncio
async def test_record_async_drive():
    with create_emulator() as emulator:

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer(FixedCompletionTime(intensity=timedelta(microseconds=50), phase=timedelta(microseconds=50))))
            autd.send(Uniform((EmitIntensity(0xFF), Phase(0x40))))
            autd.tick(timedelta(microseconds=50))
            return autd

        record = await emulator.record_async(f)

        drive = record.drive()

        assert np.array_equal(25000 * np.arange(0, 2), drive["time[ns]"])
        for dev in emulator.geometry:
            for tr in dev:
                assert np.array_equal(np.array([42, 128], np.uint8), drive[f"pulsewidth_{dev.idx}_{tr.idx}"])
                assert np.array_equal(np.array([32, 64], np.uint8), drive[f"phase_{dev.idx}_{tr.idx}"])


def test_record_output_voltage():
    with create_emulator() as emulator:

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Uniform((EmitIntensity(0xFF), Phase(0x40))))
            autd.tick(timedelta(microseconds=25))
            return autd

        record = emulator.record(f)

        drive = record.output_voltage()

        assert np.array_equal(np.arange(0, 256), drive["time[25us/256]"])
        for dev in emulator.geometry:
            for tr in dev:
                assert np.array_equal(
                    np.array(
                        [
                            12.0,
                            12.0,
                            12.0,
                            12.0,
                            12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            -12.0,
                            12.0,
                            12.0,
                            12.0,
                        ],
                        np.float32,
                    ),
                    drive[f"voltage_{dev.idx}_{tr.idx}[V]"],
                )


def test_record_output_ultrasound():
    with create_emulator() as emulator:

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Uniform((EmitIntensity(0xFF), Phase(0x40))))
            autd.tick(timedelta(microseconds=25))
            return autd

        record = emulator.record(f)

        drive = record.output_ultrasound()

        assert np.array_equal(np.arange(0, 256), drive["time[25us/256]"])
        for dev in emulator.geometry:
            for tr in dev:
                assert np.array_equal(
                    np.array(
                        [
                            0.0,
                            -0.00052675273,
                            -0.00081742747,
                            -0.00086473074,
                            -0.00072082557,
                            -0.00042681425,
                            -0.00032917314,
                            -0.00037423993,
                            -0.0005889915,
                            -0.00093673536,
                            -0.0013885288,
                            -0.0019215203,
                            -0.0025176455,
                            -0.003162602,
                            -0.0038450467,
                            -0.00455596,
                            -0.0052881516,
                            -0.006035868,
                            -0.0067944857,
                            -0.0075602704,
                            -0.008330189,
                            -0.009101757,
                            -0.0098729255,
                            -0.01064199,
                            -0.011407511,
                            -0.012168267,
                            -0.0129232025,
                            -0.013671399,
                            -0.014412044,
                            -0.015144407,
                            -0.01586783,
                            -0.016581712,
                            -0.017285492,
                            -0.01797865,
                            -0.018660694,
                            -0.019331163,
                            -0.01998961,
                            -0.020635616,
                            -0.021268772,
                            -0.021888692,
                            -0.022494998,
                            -0.023087323,
                            -0.023665318,
                            -0.024228644,
                            -0.024776971,
                            -0.025309982,
                            -0.025827369,
                            -0.026328837,
                            -0.026814101,
                            -0.027282884,
                            -0.027734926,
                            -0.02816997,
                            -0.028587773,
                            -0.028988102,
                            -0.02937074,
                            -0.029735474,
                            -0.030082105,
                            -0.030410444,
                            -0.030720312,
                            -0.031011548,
                            -0.031283997,
                            -0.03153751,
                            -0.031771958,
                            -0.031987227,
                            -0.0321832,
                            -0.032359786,
                            -0.032516897,
                            -0.03265446,
                            -0.032772418,
                            -0.03287071,
                            -0.032949306,
                            -0.033008177,
                            -0.03304731,
                            -0.0330667,
                            -0.033066362,
                            -0.03304631,
                            -0.03300657,
                            -0.0329472,
                            -0.03286825,
                            -0.032769788,
                            -0.03265189,
                            -0.03251465,
                            -0.03235817,
                            -0.03218256,
                            -0.031987946,
                            -0.03177446,
                            -0.031542256,
                            -0.03129149,
                            -0.031022325,
                            -0.030734947,
                            -0.030429542,
                            -0.030106312,
                            -0.029765472,
                            -0.029407239,
                            -0.029031843,
                            -0.02863953,
                            -0.028230552,
                            -0.027805166,
                            -0.027363643,
                            -0.026906267,
                            -0.026433324,
                            -0.025945112,
                            -0.025441939,
                            -0.024924118,
                            -0.024391975,
                            -0.023845842,
                            -0.02328606,
                            -0.022712976,
                            -0.022126945,
                            -0.02152833,
                            -0.0209175,
                            -0.020294832,
                            -0.019660711,
                            -0.019015526,
                            -0.018359674,
                            -0.017693555,
                            -0.01701758,
                            -0.016332159,
                            -0.01563771,
                            -0.01493466,
                            -0.014223433,
                            -0.013504465,
                            -0.012778191,
                            -0.012045051,
                            -0.01130549,
                            -0.010559956,
                            -0.009808898,
                            -0.009052771,
                            -0.00829203,
                            -0.0075271334,
                            -0.0067585427,
                            -0.0059867185,
                            -0.0052121254,
                            -0.004435227,
                            -0.0036564895,
                            -0.002876379,
                            -0.002095362,
                            -0.0013139049,
                            -0.00053247396,
                            0.0002484647,
                            0.0010284464,
                            0.0018070069,
                            0.0025836832,
                            0.003358015,
                            0.0041295425,
                            0.0048978087,
                            0.0056623593,
                            0.0064227423,
                            0.007178508,
                            0.0079292115,
                            0.00867441,
                            0.009413666,
                            0.010146543,
                            0.010872613,
                            0.011591448,
                            0.01230263,
                            0.013005739,
                            0.013700367,
                            0.014386106,
                            0.015062559,
                            0.015729332,
                            0.016386038,
                            0.017032294,
                            0.017667728,
                            0.018291969,
                            0.018904658,
                            0.019505443,
                            0.02009398,
                            0.020669924,
                            0.02123295,
                            0.021782735,
                            0.022318965,
                            0.022841332,
                            0.023349542,
                            0.023843307,
                            0.024322344,
                            0.024786385,
                            0.025235169,
                            0.025668444,
                            0.026085967,
                            0.026487507,
                            0.02687284,
                            0.027241753,
                            0.027594045,
                            0.027929518,
                            0.028247997,
                            0.028549304,
                            0.028833278,
                            0.029099768,
                            0.029348638,
                            0.02957975,
                            0.02979299,
                            0.029988248,
                            0.030165426,
                            0.030324439,
                            0.030465206,
                            0.030587666,
                            0.030691763,
                            0.030777454,
                            0.030844709,
                            0.030893505,
                            0.030923834,
                            0.0309357,
                            0.030929105,
                            0.030904083,
                            0.03086066,
                            0.030798886,
                            0.030718816,
                            0.030620513,
                            0.030504059,
                            0.03036954,
                            0.030217057,
                            0.030046716,
                            0.02985864,
                            0.029652957,
                            0.02942981,
                            0.029189348,
                            0.028931735,
                            0.02865714,
                            0.028365746,
                            0.028057743,
                            0.027733333,
                            0.027392725,
                            0.02703614,
                            0.026663804,
                            0.02627596,
                            0.025872855,
                            0.025454743,
                            0.025021888,
                            0.024574563,
                            0.024113052,
                            0.023637645,
                            0.023148637,
                            0.022646336,
                            0.022131054,
                            0.021603113,
                            0.02106284,
                            0.020510571,
                            0.019946644,
                            0.01937141,
                            0.018785225,
                            0.01818845,
                            0.017581448,
                            0.016964594,
                            0.016338266,
                            0.015702846,
                            0.015058722,
                            0.014406289,
                            0.013745944,
                            0.013078087,
                            0.012403126,
                            0.011721469,
                            0.011033531,
                            0.010339729,
                            0.009954547,
                            0.009799169,
                        ],
                        np.float32,
                    ),
                    drive[f"p_{dev.idx}_{tr.idx}[a.u.]"],
                )


def test_sound_field():
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).into_emulator() as emulator:

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Uniform((EmitIntensity(0xFF), Phase(0x40))))
            autd.tick(timedelta(microseconds=25 * 10))
            return autd

        record = emulator.record(f)

        sound_field = record.sound_field(
            Range(
                x_start=-1.0,
                x_end=1.0,
                y_start=0.0,
                y_end=0.0,
                z_start=10.0,
                z_end=10.0,
                resolution=1.0,
            ),
            RecordOption(
                time_step_ns=1000,
            ),
        )

        sound_field_df = sound_field.skip(timedelta(microseconds=25 * 9)).next(timedelta(microseconds=25))
        time = [int(t.replace("p[Pa]@", "").replace("[ns]", "")) for t in sound_field_df.columns[3:]]
        assert np.array_equal(np.array([-1, 0, 1], dtype=np.float32), sound_field_df["x[mm]"])
        assert np.array_equal(np.array([0, 0, 0], dtype=np.float32), sound_field_df["y[mm]"])
        assert np.array_equal(np.array([10, 10, 10], dtype=np.float32), sound_field_df["z[mm]"])
        assert np.array_equal(225000 + 1000 * np.arange(0, 25), time)
        expect = np.array(
            [
                [
                    190.96082,
                    81.954926,
                    -43.268303,
                ],
                [
                    136.85818,
                    16.451601,
                    -93.33133,
                ],
                [
                    73.53783,
                    -45.61621,
                    -141.77232,
                ],
                [
                    14.913208,
                    -93.125145,
                    -181.12187,
                ],
                [
                    -39.191376,
                    -136.62769,
                    -209.01646,
                ],
                [
                    -89.41525,
                    -176.0103,
                    -224.6327,
                ],
                [
                    -136.45963,
                    -210.92961,
                    -229.61143,
                ],
                [
                    -177.71375,
                    -232.3485,
                    -221.54436,
                ],
                [
                    -210.82788,
                    -238.78197,
                    -201.05437,
                ],
                [
                    -234.92473,
                    -235.05318,
                    -166.11269,
                ],
                [
                    -244.49503,
                    -217.45775,
                    -118.06169,
                ],
                [
                    -242.93349,
                    -189.04797,
                    -63.85608,
                ],
                [
                    -234.70769,
                    -149.43028,
                    -7.931027,
                ],
                [
                    -210.70303,
                    -101.2128,
                    52.683804,
                ],
                [
                    -170.8035,
                    -40.90981,
                    110.96725,
                ],
                [
                    -114.901855,
                    28.199083,
                    158.98596,
                ],
                [
                    -41.33793,
                    101.697235,
                    206.40062,
                ],
                [
                    37.44646,
                    166.75967,
                    243.50082,
                ],
                [
                    114.190094,
                    221.40279,
                    261.52933,
                ],
                [
                    183.8636,
                    265.89404,
                    261.34058,
                ],
                [
                    241.15149,
                    290.09818,
                    244.31012,
                ],
                [
                    284.7516,
                    294.92493,
                    215.68811,
                ],
                [
                    307.23727,
                    279.7575,
                    166.62605,
                ],
                [
                    307.96487,
                    247.80507,
                    105.14593,
                ],
                [
                    287.04877,
                    192.38678,
                    34.32131,
                ],
            ],
        )

        for i, col in enumerate(sound_field_df.columns[3:]):
            assert np.allclose(expect[i], sound_field_df[col])


@pytest.mark.asyncio
async def test_sound_field_async():
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).into_emulator() as emulator:

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Uniform((EmitIntensity(0xFF), Phase(0x40))))
            autd.tick(timedelta(microseconds=25 * 10))
            return autd

        record = emulator.record(f)

        sound_field = await record.sound_field_async(
            Range(
                x_start=-1.0,
                x_end=1.0,
                y_start=0.0,
                y_end=0.0,
                z_start=10.0,
                z_end=10.0,
                resolution=1.0,
            ),
            RecordOption(
                time_step_ns=1000,
            ),
        )

        sound_field_df = await sound_field.skip(timedelta(microseconds=25 * 9)).next_async(timedelta(microseconds=25))
        time = [int(t.replace("p[Pa]@", "").replace("[ns]", "")) for t in sound_field_df.columns[3:]]
        assert np.array_equal(np.array([-1, 0, 1], dtype=np.float32), sound_field_df["x[mm]"])
        assert np.array_equal(np.array([0, 0, 0], dtype=np.float32), sound_field_df["y[mm]"])
        assert np.array_equal(np.array([10, 10, 10], dtype=np.float32), sound_field_df["z[mm]"])
        assert np.array_equal(225000 + 1000 * np.arange(0, 25), time)
        expect = np.array(
            [
                [
                    190.96082,
                    81.954926,
                    -43.268303,
                ],
                [
                    136.85818,
                    16.451601,
                    -93.33133,
                ],
                [
                    73.53783,
                    -45.61621,
                    -141.77232,
                ],
                [
                    14.913208,
                    -93.125145,
                    -181.12187,
                ],
                [
                    -39.191376,
                    -136.62769,
                    -209.01646,
                ],
                [
                    -89.41525,
                    -176.0103,
                    -224.6327,
                ],
                [
                    -136.45963,
                    -210.92961,
                    -229.61143,
                ],
                [
                    -177.71375,
                    -232.3485,
                    -221.54436,
                ],
                [
                    -210.82788,
                    -238.78197,
                    -201.05437,
                ],
                [
                    -234.92473,
                    -235.05318,
                    -166.11269,
                ],
                [
                    -244.49503,
                    -217.45775,
                    -118.06169,
                ],
                [
                    -242.93349,
                    -189.04797,
                    -63.85608,
                ],
                [
                    -234.70769,
                    -149.43028,
                    -7.931027,
                ],
                [
                    -210.70303,
                    -101.2128,
                    52.683804,
                ],
                [
                    -170.8035,
                    -40.90981,
                    110.96725,
                ],
                [
                    -114.901855,
                    28.199083,
                    158.98596,
                ],
                [
                    -41.33793,
                    101.697235,
                    206.40062,
                ],
                [
                    37.44646,
                    166.75967,
                    243.50082,
                ],
                [
                    114.190094,
                    221.40279,
                    261.52933,
                ],
                [
                    183.8636,
                    265.89404,
                    261.34058,
                ],
                [
                    241.15149,
                    290.09818,
                    244.31012,
                ],
                [
                    284.7516,
                    294.92493,
                    215.68811,
                ],
                [
                    307.23727,
                    279.7575,
                    166.62605,
                ],
                [
                    307.96487,
                    247.80507,
                    105.14593,
                ],
                [
                    287.04877,
                    192.38678,
                    34.32131,
                ],
            ],
        )

        for i, col in enumerate(sound_field_df.columns[3:]):
            assert np.allclose(expect[i], sound_field_df[col])


def test_record_invalid_tick():
    with create_emulator() as emulator:

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Uniform((EmitIntensity(0xFF), Phase(0x40))))
            with pytest.raises(AUTDError) as e:
                autd.tick(timedelta(microseconds=1))
            assert str(e.value) == "Tick must be multiple of 25µs"
            return autd

        _ = emulator.record(f)
