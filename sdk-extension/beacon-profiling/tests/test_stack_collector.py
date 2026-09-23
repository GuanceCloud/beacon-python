from threading import Event, Thread

from pytest import MonkeyPatch

import opentelemetry.sdk.extension.profiling.collector.stack as stack_module
from opentelemetry.sdk.extension.profiling.collector.stack import (
    StackCollector,
)
from opentelemetry.sdk.extension.profiling.context_bridge import ContextBridge
from opentelemetry.sdk.trace import TracerProvider


def test_stack_collector_captures_background_thread_trace_context() -> None:
    bridge = ContextBridge()
    tracer = TracerProvider().get_tracer("test")
    ready = Event()
    finished = Event()
    captured = {}

    def worker() -> None:
        with tracer.start_as_current_span("worker-span") as span:
            captured["span_context"] = span.get_span_context()
            ready.set()
            finished.wait()

    bridge.start()
    thread = Thread(target=worker, name="worker-thread")
    thread.start()
    ready.wait(timeout=5)
    try:
        collector = StackCollector(context_bridge=bridge, max_frames=16)
        samples = collector.capture()
        matched = [
            sample
            for sample in samples
            if sample.thread_name == "worker-thread"
        ]
        assert matched
        assert matched[0].trace_id == captured["span_context"].trace_id
        assert matched[0].span_id == captured["span_context"].span_id
    finally:
        finished.set()
        thread.join(timeout=5)
        bridge.stop()


def test_stack_collector_records_thread_cpu_time_delta(
    monkeypatch: MonkeyPatch,
) -> None:
    bridge = ContextBridge()
    ready = Event()
    finished = Event()

    def worker() -> None:
        ready.set()
        finished.wait()

    thread = Thread(target=worker, name="cpu-worker")
    thread.start()
    ready.wait(timeout=5)
    assert thread.ident is not None
    readings = iter((100, 350))
    monkeypatch.setattr(
        stack_module,
        "_read_thread_cpu_time_ns",
        lambda thread_id: (
            next(readings) if thread_id == thread.ident else None
        ),
    )

    try:
        collector = StackCollector(
            context_bridge=bridge,
            max_frames=16,
            include_trace_context=False,
        )
        collector.capture()
        samples = collector.capture()
        matched = [
            sample for sample in samples if sample.thread_name == "cpu-worker"
        ]

        assert matched
        assert matched[0].cpu_time_ns == 250
    finally:
        finished.set()
        thread.join(timeout=5)


def test_stack_collector_excludes_profiler_scheduler_thread() -> None:
    ready = Event()
    finished = Event()

    def worker() -> None:
        ready.set()
        finished.wait()

    thread = Thread(target=worker, name="OTelProfileScheduler")
    thread.start()
    ready.wait(timeout=5)

    try:
        collector = StackCollector(
            context_bridge=ContextBridge(),
            include_trace_context=False,
        )

        samples = collector.capture()

        assert all(
            sample.thread_name != "OTelProfileScheduler" for sample in samples
        )
    finally:
        finished.set()
        thread.join(timeout=5)
