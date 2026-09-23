from __future__ import annotations

from threading import Event

from opentelemetry.sdk.extension.profiling.collector.base import CapturedSample
from opentelemetry.sdk.extension.profiling.runtime import Profiler


class _NoopExporter:
    def export(self, payload: bytes) -> None:
        del payload

    def shutdown(self) -> None:
        return None


class _BlockingMemoryCollector:
    def __init__(self) -> None:
        self.entered = Event()
        self.release = Event()

    def start(self) -> None:
        return None

    def stop(self) -> None:
        return None

    def capture(self) -> list[CapturedSample]:
        self.entered.set()
        self.release.wait(timeout=2)
        return []


class _StackCollector:
    def __init__(self, memory_collector: _BlockingMemoryCollector) -> None:
        self._memory_collector = memory_collector
        self.captured_while_memory_blocked = Event()

    def start(self) -> None:
        return None

    def stop(self) -> None:
        return None

    def capture(self) -> list[CapturedSample]:
        if (
            self._memory_collector.entered.is_set()
            and not self._memory_collector.release.is_set()
        ):
            self.captured_while_memory_blocked.set()
        return []


def test_memory_capture_does_not_block_regular_stack_sampling() -> None:
    memory_collector = _BlockingMemoryCollector()
    stack_collector = _StackCollector(memory_collector)
    profiler = Profiler(
        exporter=_NoopExporter(),
        sample_interval=0.005,
        export_interval=60.0,
        memory_interval=0.005,
    )
    profiler._collectors = [stack_collector]
    profiler._memory_collector = memory_collector

    try:
        profiler.start()
        assert memory_collector.entered.wait(timeout=1)
        assert stack_collector.captured_while_memory_blocked.wait(timeout=1)
    finally:
        memory_collector.release.set()
        profiler.stop(flush=False)
