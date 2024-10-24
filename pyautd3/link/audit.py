import ctypes
from typing import Self

import numpy as np

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3_driver import Drive as Drive_
from pyautd3.native_methods.autd3capi import NativeMethods as LinkAudit
from pyautd3.native_methods.autd3capi_driver import ControllerPtr, HandlePtr, LinkBuilderPtr, LinkPtr, LoopBehavior, Segment, SilencerTarget

__all__ = []  # type: ignore[var-annotated]


class Audit(Link):
    _ptr: LinkPtr

    class _Builder(LinkBuilder["Audit"]):
        def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
            return LinkAudit().link_audit()

        def _resolve_link(self: Self, handle: HandlePtr, ptr: ControllerPtr) -> "Audit":
            return Audit(handle, LinkAudit().link_get(ptr))

    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)

    @staticmethod
    def builder() -> _Builder:
        return Audit._Builder()

    def down(self: Self) -> None:
        LinkAudit().link_audit_down(self._ptr)

    def up(self: Self) -> None:
        LinkAudit().link_audit_up(self._ptr)

    def is_open(self: Self) -> bool:
        return bool(LinkAudit().link_audit_is_open(self._ptr))

    def is_force_fan(self: Self, idx: int) -> bool:
        return bool(LinkAudit().link_audit_fpga_is_force_fan(self._ptr, idx))

    def break_down(self: Self) -> None:
        LinkAudit().link_audit_break_down(self._ptr)

    def repair(self: Self) -> None:
        LinkAudit().link_audit_repair(self._ptr)

    def silencer_strict_mode(self: Self, idx: int) -> bool:
        return bool(LinkAudit().link_audit_cpu_silencer_strict_mode(self._ptr, idx))

    def silencer_update_rate_intensity(self: Self, idx: int) -> int:
        return int(LinkAudit().link_audit_fpga_silencer_update_rate_intensity(self._ptr, idx))

    def silencer_update_rate_phase(self: Self, idx: int) -> int:
        return int(LinkAudit().link_audit_fpga_silencer_update_rate_phase(self._ptr, idx))

    def silencer_completion_steps_intensity(self: Self, idx: int) -> int:
        return int(LinkAudit().link_audit_fpga_silencer_completion_steps_intensity(self._ptr, idx))

    def silencer_completion_steps_phase(self: Self, idx: int) -> int:
        return int(LinkAudit().link_audit_fpga_silencer_completion_steps_phase(self._ptr, idx))

    def silencer_fixed_completion_steps_mode(self: Self, idx: int) -> bool:
        return bool(LinkAudit().link_audit_fpga_silencer_fixed_completion_steps_mode(self._ptr, idx))

    def silencer_target(self: Self, idx: int) -> SilencerTarget:
        return LinkAudit().link_audit_fpga_silencer_target(self._ptr, idx)

    def debug_types(self: Self, idx: int) -> np.ndarray:
        buf = np.zeros([4]).astype(ctypes.c_uint8)
        LinkAudit().link_audit_fpga_debug_types(self._ptr, idx, np.ctypeslib.as_ctypes(buf))
        return buf

    def debug_values(self: Self, idx: int) -> np.ndarray:
        buf = np.zeros([4]).astype(ctypes.c_uint64)
        LinkAudit().link_audit_fpga_debug_values(self._ptr, idx, np.ctypeslib.as_ctypes(buf))
        return buf

    def assert_thermal_sensor(self: Self, idx: int) -> None:
        LinkAudit().link_audit_fpga_assert_thermal_sensor(self._ptr, idx)

    def deassert_thermal_sensor(self: Self, idx: int) -> None:
        LinkAudit().link_audit_fpga_deassert_thermal_sensor(self._ptr, idx)

    def modulation_buffer(
        self: Self,
        idx: int,
        segment: Segment,
    ) -> np.ndarray:
        n = int(LinkAudit().link_audit_fpga_modulation_cycle(self._ptr, segment, idx))
        buf = np.zeros([n]).astype(ctypes.c_uint8)
        LinkAudit().link_audit_fpga_modulation_buffer(self._ptr, segment, idx, np.ctypeslib.as_ctypes(buf), n)
        return buf

    def modulation_frequency_division(self: Self, idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_modulation_freq_division(self._ptr, segment, idx))

    def modulation_loop_behavior(self: Self, idx: int, segment: Segment) -> LoopBehavior:
        return LinkAudit().link_audit_fpga_modulation_loop_behavior(self._ptr, segment, idx)

    def drives_at(self: Self, idx: int, segment: Segment, stm_idx: int) -> tuple[np.ndarray, np.ndarray]:
        n = int(LinkAudit().link_audit_cpu_num_transducers(self._ptr, idx))
        drive = np.zeros(n, dtype=Drive_)
        LinkAudit().link_audit_fpga_drives_at(
            self._ptr,
            segment,
            idx,
            stm_idx,
            drive.ctypes.data_as(ctypes.POINTER(Drive_)),  # type: ignore[arg-type]
        )
        return np.array([int(d[1]) for d in drive]), np.array([int(d[0]) for d in drive])

    def sound_speed(self: Self, idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_sound_speed(self._ptr, segment, idx))

    def stm_cycle(self: Self, idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_stm_cycle(self._ptr, segment, idx))

    def is_stm_gain_mode(self: Self, idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_is_stm_gain_mode(self._ptr, segment, idx))

    def stm_freqency_division(self: Self, idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_stm_freq_division(self._ptr, segment, idx))

    def stm_loop_behavior(self: Self, idx: int, segment: Segment) -> LoopBehavior:
        return LinkAudit().link_audit_fpga_stm_loop_behavior(self._ptr, segment, idx)

    def current_stm_segment(self: Self, idx: int) -> Segment:
        return LinkAudit().link_audit_fpga_current_stm_segment(self._ptr, idx)

    def current_mod_segment(self: Self, idx: int) -> Segment:
        return LinkAudit().link_audit_fpga_current_mod_segment(self._ptr, idx)

    def pulse_width_encoder_table(self: Self, idx: int) -> np.ndarray:
        p = np.zeros([256]).astype(ctypes.c_uint8)
        LinkAudit().link_audit_fpga_pulse_width_encoder_table(
            self._ptr,
            idx,
            np.ctypeslib.as_ctypes(p),
        )
        return p
