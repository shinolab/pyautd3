import ctypes
from datetime import timedelta

import numpy as np

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr, LinkAuditBuilderPtr, RuntimePtr
from pyautd3.native_methods.autd3capi import NativeMethods as LinkAudit
from pyautd3.native_methods.autd3capi_driver import LinkBuilderPtr, LinkPtr, LoopBehavior, Segment, SilencerTarget

__all__ = []  # type: ignore[var-annotated]


class Audit(Link):
    _ptr: LinkPtr

    class _Builder(LinkBuilder["Audit"]):
        _builder: LinkAuditBuilderPtr

        def __init__(self: "Audit._Builder") -> None:
            self._builder = LinkAudit().link_audit()

        def with_timeout(self: "Audit._Builder", timeout: timedelta) -> "Audit._Builder":
            self._builder = LinkAudit().link_audit_with_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def _link_builder_ptr(self: "Audit._Builder") -> LinkBuilderPtr:
            return LinkAudit().link_audit_into_builder(self._builder)

        def _resolve_link(self: "Audit._Builder", runtime: RuntimePtr, ptr: ControllerPtr) -> "Audit":
            return Audit(runtime, LinkAudit().link_get(ptr))

    def __init__(self: "Audit", runtime: RuntimePtr, ptr: LinkPtr) -> None:
        super().__init__(runtime, ptr)

    @staticmethod
    def builder() -> _Builder:
        return Audit._Builder()

    def down(self: "Audit") -> None:
        LinkAudit().link_audit_down(self._ptr)

    def up(self: "Audit") -> None:
        LinkAudit().link_audit_up(self._ptr)

    def is_open(self: "Audit") -> bool:
        return bool(LinkAudit().link_audit_is_open(self._ptr))

    def is_force_fan(self: "Audit", idx: int) -> bool:
        return bool(LinkAudit().link_audit_fpga_is_force_fan(self._ptr, idx))

    def break_down(self: "Audit") -> None:
        LinkAudit().link_audit_break_down(self._ptr)

    def repair(self: "Audit") -> None:
        LinkAudit().link_audit_repair(self._ptr)

    def timeout(self: "Audit") -> timedelta:
        return timedelta(microseconds=int(LinkAudit().link_audit_timeout_ns(self._ptr)) / 1000)

    def last_timeout(self: "Audit") -> timedelta | None:
        us = int(LinkAudit().link_audit_last_timeout_ns(self._ptr)) / 1000
        return None if us < 0 else timedelta(microseconds=us)

    def silencer_strict_mode(self: "Audit", idx: int) -> bool:
        return bool(LinkAudit().link_audit_cpu_silencer_strict_mode(self._ptr, idx))

    def silencer_update_rate_intensity(self: "Audit", idx: int) -> int:
        return int(LinkAudit().link_audit_fpga_silencer_update_rate_intensity(self._ptr, idx))

    def silencer_update_rate_phase(self: "Audit", idx: int) -> int:
        return int(LinkAudit().link_audit_fpga_silencer_update_rate_phase(self._ptr, idx))

    def silencer_completion_steps_intensity(self: "Audit", idx: int) -> int:
        return int(LinkAudit().link_audit_fpga_silencer_completion_steps_intensity(self._ptr, idx))

    def silencer_completion_steps_phase(self: "Audit", idx: int) -> int:
        return int(LinkAudit().link_audit_fpga_silencer_completion_steps_phase(self._ptr, idx))

    def silencer_fixed_completion_steps_mode(self: "Audit", idx: int) -> bool:
        return bool(LinkAudit().link_audit_fpga_silencer_fixed_completion_steps_mode(self._ptr, idx))

    def silencer_target(self: "Audit", idx: int) -> SilencerTarget:
        return LinkAudit().link_audit_fpga_silencer_target(self._ptr, idx)

    def debug_types(self: "Audit", idx: int) -> np.ndarray:
        buf = np.zeros([4]).astype(ctypes.c_uint8)
        LinkAudit().link_audit_fpga_debug_types(self._ptr, idx, np.ctypeslib.as_ctypes(buf))
        return buf

    def debug_values(self: "Audit", idx: int) -> np.ndarray:
        buf = np.zeros([4]).astype(ctypes.c_uint16)
        LinkAudit().link_audit_fpga_debug_values(self._ptr, idx, np.ctypeslib.as_ctypes(buf))
        return buf

    def assert_thermal_sensor(self: "Audit", idx: int) -> None:
        LinkAudit().link_audit_fpga_assert_thermal_sensor(self._ptr, idx)

    def deassert_thermal_sensor(self: "Audit", idx: int) -> None:
        LinkAudit().link_audit_fpga_deassert_thermal_sensor(self._ptr, idx)

    def modulation(
        self: "Audit",
        idx: int,
        segment: Segment,
    ) -> np.ndarray:
        n = int(LinkAudit().link_audit_fpga_modulation_cycle(self._ptr, segment, idx))
        buf = np.zeros([n]).astype(ctypes.c_uint8)
        LinkAudit().link_audit_fpga_modulation(self._ptr, segment, idx, np.ctypeslib.as_ctypes(buf))
        return buf

    def modulation_frequency_division(self: "Audit", idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_modulation_freq_division(self._ptr, segment, idx))

    def modulation_loop_behavior(self: "Audit", idx: int, segment: Segment) -> LoopBehavior:
        return LinkAudit().link_audit_fpga_modulation_loop_behavior(self._ptr, segment, idx)

    def drives(self: "Audit", idx: int, segment: Segment, stm_idx: int) -> tuple[np.ndarray, np.ndarray]:
        n = int(LinkAudit().link_audit_cpu_num_transducers(self._ptr, idx))
        intensities = np.zeros([n]).astype(ctypes.c_uint8)
        phases = np.zeros([n]).astype(ctypes.c_uint8)
        LinkAudit().link_audit_fpga_drives(
            self._ptr,
            segment,
            idx,
            stm_idx,
            np.ctypeslib.as_ctypes(intensities),
            np.ctypeslib.as_ctypes(phases),
        )
        return (intensities, phases)

    def sound_speed(self: "Audit", idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_sound_speed(self._ptr, segment, idx))

    def stm_cycle(self: "Audit", idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_stm_cycle(self._ptr, segment, idx))

    def is_stm_gain_mode(self: "Audit", idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_is_stm_gain_mode(self._ptr, segment, idx))

    def stm_freqency_division(self: "Audit", idx: int, segment: Segment) -> int:
        return int(LinkAudit().link_audit_fpga_stm_freq_division(self._ptr, segment, idx))

    def stm_loop_behavior(self: "Audit", idx: int, segment: Segment) -> LoopBehavior:
        return LinkAudit().link_audit_fpga_stm_loop_behavior(self._ptr, segment, idx)

    def current_stm_segment(self: "Audit", idx: int) -> Segment:
        return LinkAudit().link_audit_fpga_current_stm_segment(self._ptr, idx)

    def current_mod_segment(self: "Audit", idx: int) -> Segment:
        return LinkAudit().link_audit_fpga_current_mod_segment(self._ptr, idx)

    def pulse_width_encoder_table(self: "Audit", idx: int) -> np.ndarray:
        p = np.zeros([256]).astype(ctypes.c_uint8)
        LinkAudit().link_audit_fpga_pulse_width_encoder_table(
            self._ptr,
            idx,
            np.ctypeslib.as_ctypes(p),
        )
        return p
